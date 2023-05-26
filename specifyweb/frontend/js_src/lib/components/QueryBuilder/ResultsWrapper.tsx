import React from 'react';

import { ajax } from '../../utils/ajax';
import { runQuery } from '../../utils/ajax/specifyApi';
import type { RA } from '../../utils/types';
import { keysToLowerCase, replaceItem } from '../../utils/utils';
import { serializeResource } from '../DataModel/helpers';
import type { SerializedResource } from '../DataModel/helperTypes';
import type { SpecifyResource } from '../DataModel/legacyTypes';
import type { SpecifyModel } from '../DataModel/specifyModel';
import type { SpQuery, SpQueryField, Tables } from '../DataModel/types';
import { raise } from '../Errors/Crash';
import { ErrorBoundary } from '../Errors/ErrorBoundary';
import { loadingGif } from '../Molecules';
import type { QueryField } from './helpers';
import {
  addFormattedField,
  augmentQueryFields,
  queryFieldsToFieldSpecs,
  unParseQueryFields,
} from './helpers';
import { QueryResults } from './Results';
import { mappingPathIsComplete } from '../WbPlanView/helpers';

// TODO: [FEATURE] allow customizing this and other constants as make sense
const fetchSize = 40;

export function QueryResultsWrapper({
  baseTableName,
  model,
  queryRunCount,
  queryResource,
  fields,
  recordSetId,
  createRecordSet,
  extraButtons,
  forceCollection,
  onSelected: handleSelected,
  onSortChange: handleSortChange,
  onReRun: handleReRun,
}: {
  readonly baseTableName: keyof Tables;
  readonly model: SpecifyModel;
  readonly queryRunCount: number;
  readonly queryResource: SpecifyResource<SpQuery>;
  readonly fields: RA<QueryField>;
  readonly recordSetId: number | undefined;
  readonly createRecordSet: JSX.Element | undefined;
  readonly extraButtons: JSX.Element | undefined;
  readonly forceCollection: number | undefined;
  readonly onSelected?: (selected: RA<number>) => void;
  readonly onSortChange?: (
    /*
     * Since this component may add fields to the query, it needs to send back
     * all of the fields
     */
    newFields: RA<QueryField>
  ) => void;
  readonly onReRun: () => void;
}): JSX.Element | null {
  const fetchResults = React.useCallback(
    async (fields: RA<SerializedResource<SpQueryField>>, offset: number) =>
      runQuery(
        {
          ...serializeResource(queryResource),
          fields,
        },
        {
          collectionId: forceCollection,
          recordSetId,
          limit: fetchSize,
          offset,
        }
      ),
    [forceCollection, fields, baseTableName, queryResource, recordSetId]
  );

  /*
   * Need to store all props in a state so that query field edits do not affect
   * the query results until query is reRun
   */
  const [props, setProps] = React.useState<
    | Omit<Parameters<typeof QueryResults>[0], 'onReRun' | 'totalCount'>
    | undefined
  >(undefined);

  const [totalCount, setTotalCount] = React.useState<number | undefined>(
    undefined
  );

  const previousQueryRunCount = React.useRef(0);
  React.useEffect(() => {
    if (queryRunCount === previousQueryRunCount.current) return;
    previousQueryRunCount.current = queryRunCount;
    // Display the loading GIF
    setProps(undefined);

    const countOnly = queryResource.get('countOnly') === true;
    const augmentedFields = augmentQueryFields(
      baseTableName,
      fields.filter(({ mappingPath }) => mappingPathIsComplete(mappingPath)),
      queryResource.get('selectDistinct')
    );
    const allFields = addFormattedField(augmentedFields);
    const unParsedFields = unParseQueryFields(baseTableName, allFields);

    setTotalCount(undefined);
    ajax<{ readonly count: number }>('/stored_query/ephemeral/', {
      method: 'POST',
      // eslint-disable-next-line @typescript-eslint/naming-convention
      headers: { Accept: 'application/json' },
      errorMode: 'dismissible',
      body: keysToLowerCase({
        ...queryResource.toJSON(),
        collectionId: forceCollection,
        fields: unParsedFields,
        recordSetId,
        countOnly: true,
      }),
    })
      .then(({ data }) => setTotalCount(data.count))
      .catch(raise);

    const displayedFields = allFields.filter((field) => field.isDisplay);
    const isCountOnly =
      countOnly ||
      // Run as "count only" if there are no visible fields
      displayedFields.length === 0;
    const initialData = isCountOnly
      ? Promise.resolve(undefined)
      : fetchResults(unParsedFields, 0);
    const fieldSpecs = queryFieldsToFieldSpecs(
      baseTableName,
      displayedFields
    ).map(([_field, fieldSpec]) => fieldSpec);

    initialData
      .then((initialData) =>
        setProps({
          model,
          hasIdField: queryResource.get('selectDistinct') !== true,
          queryResource,
          fetchSize,
          fetchResults: isCountOnly
            ? undefined
            : fetchResults.bind(undefined, unParsedFields),
          fieldSpecs,
          initialData,
          sortConfig: fields
            .filter(({ isDisplay }) => isDisplay)
            .map((field) => field.sortType),
          onSortChange:
            typeof handleSortChange === 'function'
              ? (fieldSpec, sortType) => {
                  /*
                   * If some fields are not displayed, visual index and actual field
                   * index differ
                   */
                  const index = fieldSpecs.indexOf(fieldSpec);
                  const field = displayedFields[index];
                  handleSortChange(
                    replaceItem(allFields, index, {
                      ...field,
                      sortType,
                    })
                  );
                }
              : undefined,
          createRecordSet,
          extraButtons,
          onSelected: handleSelected,
        })
      )
      .catch(raise);
  }, [
    fields,
    baseTableName,
    fetchResults,
    forceCollection,
    queryResource,
    queryRunCount,
    recordSetId,
    model,
  ]);

  return props === undefined ? (
    queryRunCount === 0 ? null : (
      <div className="flex-1 snap-start">{loadingGif}</div>
    )
  ) : (
    <div className="flex flex-1 snap-start overflow-hidden">
      <ErrorBoundary dismissible>
        <QueryResults
          {...props}
          totalCount={totalCount}
          onReRun={handleReRun}
        />
      </ErrorBoundary>
    </div>
  );
}
