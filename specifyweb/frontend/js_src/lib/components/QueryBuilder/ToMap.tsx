import type L from 'leaflet';
import React from 'react';

import { useBooleanState } from '../../hooks/useBooleanState';
import { commonText } from '../../localization/common';
import { queryText } from '../../localization/query';
import { eventListener } from '../../utils/events';
import { f } from '../../utils/functools';
import type { RA, WritableArray } from '../../utils/types';
import { filterArray } from '../../utils/types';
import { Progress } from '../Atoms';
import { Button } from '../Atoms/Button';
import { formatNumber } from '../Atoms/Internationalization';
import { schema } from '../DataModel/schema';
import type { SpecifyModel } from '../DataModel/specifyModel';
import type { Tables } from '../DataModel/types';
import { softFail } from '../Errors/Crash';
import {
  formatLocalityData,
  getMarkersFromLocalityData,
} from '../Leaflet/leaflet';
import type { LeafletInstance } from '../Leaflet/leafletAddOns';
import { queryMappingLocalityColumns } from '../Leaflet/leafletConfig';
import type { LocalityData } from '../Leaflet/leafletHelpers';
import {
  fetchLocalityDataFromResource,
  formatLocalityDataObject,
} from '../Leaflet/localityRecordDataExtractor';
import { findLocalityColumnsInDataSet } from '../Leaflet/wbLocalityDataExtractor';
import { LoadingScreen } from '../Molecules/Dialog';
import { LeafletMap } from '../Molecules/Leaflet';
import { defaultColumnOptions } from '../WbPlanView/linesGetter';
import type { SplitMappingPath } from '../WbPlanView/mappingHelpers';
import {
  mappingPathToString,
  splitJoinedMappingPath,
} from '../WbPlanView/mappingHelpers';
import type { QueryFieldSpec } from './fieldSpec';
import type { QueryResultRow } from './Results';
import { queryIdField } from './Results';

export function QueryToMap({
  results,
  totalCount,
  selectedRows,
  model,
  fieldSpecs,
  onFetchMore: handleFetchMore,
}: {
  readonly results: RA<QueryResultRow>;
  readonly totalCount: number | undefined;
  readonly selectedRows: ReadonlySet<number>;
  readonly model: SpecifyModel;
  readonly fieldSpecs: RA<QueryFieldSpec>;
  readonly onFetchMore: (() => Promise<RA<QueryResultRow> | void>) | undefined;
}): JSX.Element | null {
  const [isOpen, handleOpen, handleClose] = useBooleanState();
  const ids = useSelectedResults(results, selectedRows);
  const localityMappings = useLocalityMappings(model.name, fieldSpecs);
  return localityMappings.length === 0 ? null : (
    <>
      <Button.Small disabled={results.length === 0} onClick={handleOpen}>
        {commonText('geoMap')}
      </Button.Small>
      {isOpen && ids.length > 0 ? (
        <Dialog
          localityMappings={localityMappings}
          results={results}
          totalCount={totalCount}
          onClose={handleClose}
          onFetchMore={selectedRows.size > 0 ? undefined : handleFetchMore}
        />
      ) : undefined}
    </>
  );
}

function useSelectedResults(
  results: RA<QueryResultRow | undefined>,
  selectedRows: ReadonlySet<number>
): RA<QueryResultRow | undefined> {
  return React.useMemo(
    () =>
      selectedRows.size === 0
        ? results
        : results.filter((result) =>
            f.has(selectedRows, result?.[queryIdField])
          ),
    [results, selectedRows]
  );
}

type LocalityColumn = {
  readonly localityColumn: string;
  readonly columnIndex: number;
};

function useLocalityMappings(
  tableName: keyof Tables,
  fieldSpecs: RA<QueryFieldSpec>
): RA<RA<LocalityColumn>> {
  return React.useMemo(() => {
    const splitPaths = fieldSpecsToMappingPaths(fieldSpecs);
    const mappingPaths = splitPaths.map(({ mappingPath }) =>
      mappingPathToString(mappingPath)
    );
    return findLocalityColumnsInDataSet(tableName, splitPaths).map(
      (localityColumns) => {
        const mapped = Object.entries(localityColumns)
          .filter(([key]) => queryMappingLocalityColumns.includes(key))
          .map(([localityColumn, mapping]) => {
            const pathToLocalityField = splitJoinedMappingPath(localityColumn);
            if (pathToLocalityField.length !== 2)
              throw new Error('Only direct locality fields are supported');
            const fieldName = pathToLocalityField.at(-1)!;
            return {
              localityColumn: fieldName,
              columnIndex: mappingPaths.indexOf(mapping),
            };
          });

        const basePath = splitJoinedMappingPath(
          localityColumns['locality.longitude1']
        ).slice(0, -1);
        const idPath = mappingPathToString([...basePath, 'localityId']);
        return [
          ...mapped,
          {
            localityColumn: 'localityId',
            columnIndex: mappingPaths.indexOf(idPath),
          },
        ];
      }
    );
  }, [tableName, fieldSpecs]);
}

const fieldSpecsToMappingPaths = (
  fieldSpecs: RA<QueryFieldSpec>
): RA<SplitMappingPath> =>
  fieldSpecs
    .map((fieldSpec) => fieldSpec.toMappingPath())
    .map((mappingPath) => ({
      headerName: mappingPathToString(mappingPath),
      mappingPath,
      columnOptions: defaultColumnOptions,
    }));

type LocalityDataWithId = {
  readonly localityId: number;
  readonly localityData: LocalityData;
};

function Dialog({
  results,
  totalCount,
  localityMappings,
  onClose: handleClose,
  onFetchMore: handleFetchMore,
}: {
  readonly results: RA<QueryResultRow>;
  readonly totalCount: number | undefined;
  readonly localityMappings: RA<RA<LocalityColumn>>;
  readonly onClose: () => void;
  readonly onFetchMore: (() => Promise<RA<QueryResultRow> | void>) | undefined;
}): JSX.Element {
  const [map, setMap] = React.useState<LeafletInstance | null>(null);
  const localityData = React.useRef<RA<LocalityDataWithId>>([]);
  const [initialData, setInitialData] = React.useState<
    | {
        readonly localityData: RA<LocalityData>;
        readonly onClick: ReturnType<typeof createClickCallback>;
      }
    | undefined
  >(undefined);

  const markerEvents = React.useMemo(
    () => eventListener<{ readonly updated: undefined }>(),
    []
  );

  const handleAddPoints = React.useCallback(
    (results: RA<QueryResultRow>) => {
      /*
       * Need to add markers into queue rather than directly to the map because
       * the map might not be initialized yet (the map is only initialized after
       * some markers are fetched, so that it can open to correct position)
       */
      localityData.current = [
        ...localityData.current,
        ...extractLocalities(results, localityMappings),
      ];
      setInitialData((initialData) =>
        typeof initialData === 'object'
          ? initialData
          : {
              localityData: localityData.current.map(
                ({ localityData }) => localityData
              ),
              onClick: createClickCallback(localityData.current),
            }
      );
      markerEvents.trigger('updated');
    },
    [localityMappings, markerEvents]
  );

  // Add initial results
  React.useEffect(() => handleAddPoints(results), [handleAddPoints]);
  useFetchLoop(handleFetchMore, handleAddPoints);

  React.useEffect(() => {
    if (map === null) return undefined;

    function emptyQueue(): void {
      if (map === null) return;
      addLeafletMarkers(map, localityData.current);
      localityData.current = [];
    }

    return markerEvents.on('updated', emptyQueue, true);
  }, [map, markerEvents]);

  return typeof initialData === 'object' ? (
    <LeafletMap
      /*
       * This will only add initial locality data
       * That is needed so that the map can zoom in to correct place
       */
      forwardRef={setMap}
      header={`${commonText('geoMap')}${
        typeof totalCount === 'number'
          ? results.length === totalCount
            ? queryText('queryMapAll', formatNumber(results.length))
            : ` - ${queryText(
                'queryMapSubset',
                formatNumber(results.length),
                formatNumber(totalCount)
              )}`
          : ''
      }`}
      headerButtons={
        typeof totalCount === 'number' && totalCount !== results.length ? (
          <Progress
            className="flex-1"
            aria-hidden
            max={totalCount}
            value={results.length}
          />
        ) : undefined
      }
      localityPoints={initialData.localityData}
      onClose={handleClose}
      onMarkerClick={initialData.onClick}
    />
  ) : (
    <LoadingScreen />
  );
}

const extractLocalities = (
  results: RA<QueryResultRow>,
  localityMappings: RA<RA<LocalityColumn>>
): RA<{ readonly localityId: number; readonly localityData: LocalityData }> =>
  filterArray(
    results.flatMap((row) =>
      localityMappings.map((mappings) => {
        const fields = mappings.map(
          ({ localityColumn, columnIndex }) =>
            [
              [localityColumn],
              // "+1" is to compensate for queryIdField
              row[columnIndex + 1]?.toString() ?? null,
            ] as const
        );
        const localityData = formatLocalityDataObject(fields);
        const localityId = f.parseInt(
          fields.find(
            ([localityColumn]) => localityColumn[0] === 'localityId'
          )?.[1] ?? undefined
        );
        return localityData === false || typeof localityId !== 'number'
          ? undefined
          : { localityId, localityData };
      })
    )
  );

function createClickCallback(
  points: RA<LocalityDataWithId>
): (index: number, event: L.LeafletEvent) => Promise<void> {
  const fullLocalityData: WritableArray<LocalityData | false | undefined> = [];

  return async (index, { target: marker }): Promise<void> => {
    const resource = new schema.models.Locality.Resource({
      id: points[index].localityId,
    });
    fullLocalityData[index] ??= await fetchLocalityDataFromResource(resource);
    const localityData = fullLocalityData[index];
    if (localityData !== false)
      (marker as L.Marker)
        .getPopup()
        ?.setContent(
          formatLocalityData(localityData!, resource.viewUrl(), true)
        );
  };
}

function addLeafletMarkers(
  map: LeafletInstance,
  points: RA<LocalityDataWithId>
): void {
  if (points.length === 0) return;

  const handleMarkerClick = createClickCallback(points);

  const markers = points.map(({ localityData }, index) =>
    getMarkersFromLocalityData({
      localityData,
      onMarkerClick: handleMarkerClick.bind(undefined, index),
    })
  );

  map.addMarkers(markers);
}

/**
 * Fetch query results until all are fetched
 */
function useFetchLoop(
  handleFetchMore: (() => Promise<RA<QueryResultRow> | void>) | undefined,
  handleAdd: (results: RA<QueryResultRow>) => void
): void {
  const [lastResults, setLastResults] =
    React.useState<RA<QueryResultRow> | void>(undefined);
  React.useEffect(
    () =>
      void handleFetchMore?.()
        .then((results) => {
          setLastResults(results);
          f.maybe(results, handleAdd);
        })
        .catch(softFail),
    [handleFetchMore, handleAdd, lastResults]
  );
}
