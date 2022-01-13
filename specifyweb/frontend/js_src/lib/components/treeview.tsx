import * as React from 'react';

import ajax from '../ajax';
import type { SpecifyResource } from '../legacytypes';
import commonText from '../localization/common';
import treeText from '../localization/tree';
import * as navigation from '../navigation';
import * as querystring from '../querystring';
import { getIntPref, getPref } from '../remoteprefs';
import { getModel } from '../schema';
import type { RA, RR } from '../types';
import { defined } from '../types';
import { capitalize } from '../wbplanviewhelper';
import { Autocomplete } from './autocomplete';
import { Button, className } from './basic';
import { useId, useTitle } from './hooks';
import icons from './icons';
import { formatNumber } from './internationalization';
import { LoadingScreen } from './modaldialog';
import createBackboneView from './reactbackboneextend';
import { useCachedState } from './stateCache';

const fetchRows = async (fetchUrl: string) =>
  ajax<
    RA<
      Readonly<
        [
          number,
          string,
          string,
          number,
          number,
          number,
          number | null,
          string | null,
          number
        ]
      >
    >
  >(fetchUrl, {
    // eslint-disable-next-line @typescript-eslint/naming-convention
    headers: { Accept: 'application/json' },
  }).then(({ data: rows }) =>
    rows.map(
      (
        [
          nodeId,
          name,
          fullName,
          nodeNumber,
          highestNodeNumber,
          rankId,
          acceptedId,
          acceptedName,
          children,
        ],
        index,
        { length }
      ) => ({
        nodeId,
        name,
        fullName,
        nodeNumber,
        highestNodeNumber,
        rankId,
        acceptedId: acceptedId ?? undefined,
        acceptedName: acceptedName ?? undefined,
        children,
        isLastChild: index + 1 === length,
      })
    )
  );

type Stats = RR<
  number,
  {
    readonly directCount: number;
    readonly childCount: number;
  }
>;

const fetchStats = async (url: string): Promise<Stats> =>
  ajax<RA<Readonly<[number, number, number]>>>(url, {
    // eslint-disable-next-line @typescript-eslint/naming-convention
    headers: { Accept: 'application/json' },
  }).then(({ data }) =>
    Object.fromEntries(
      data.map(([childId, directCount, allCount]) => [
        childId,
        {
          directCount,
          childCount: allCount - directCount,
        },
      ])
    )
  );

type Row = Awaited<ReturnType<typeof fetchRows>>[number];

/**
 * Conditional Pipe. Like Ramda's lenses
 */
const pipe = <T, V>(
  value: T,
  condition: boolean,
  mapper: (value: T) => V
): T | V => (condition ? mapper(value) : value);

/*
 * TODO: hide root rank if it is the only one
 * TODO: replace context menu with an accessible solution
 */

type Conformations = RA<Conformation>;

interface Conformation extends Readonly<[number, ...Conformations]> {}

function deserializeConformation(
  conformation: string | undefined
): Conformations | undefined {
  if (typeof conformation === 'undefined') return undefined;
  const serialized = conformation
    .replace(/([^~])~/g, '$1,~')
    .replaceAll('~', '[')
    .replaceAll('-', ']');
  try {
    return JSON.parse(serialized) as Conformations;
  } catch {
    console.error('bad tree conformation:', serialized);
    return undefined;
  }
}

/**
 * Replace reserved url characters to avoid percent
 * escaping.  Also, commas are superfluous since they
 * precede every open bracket that is not itself preceded
 * by an open bracket by nature of the construction.
 */
const serializeConformation = (
  conformation: Conformations | undefined
): string =>
  JSON.stringify(conformation)
    .replaceAll('[', '~')
    .replaceAll(']', '-')
    .replaceAll(',', '');

function TreeView({
  tableName,
  treeDefinition,
  treeDefinitionItems,
}: {
  readonly tableName: string;
  readonly treeDefinition: SpecifyResource;
  readonly treeDefinitionItems: RA<SpecifyResource>;
}): JSX.Element {
  const table = defined(getModel(tableName));
  const rankIds = treeDefinitionItems.map((rank) => rank.get<number>('rankid'));
  const [collapsedRanks, setCollapsedRanks] = useCachedState({
    bucketName: 'tree',
    cacheName: `collapsedRanks${capitalize(tableName)}`,
    bucketType: 'localStorage',
    defaultValue: [],
  });

  const [rawConformation, setConformation] = useCachedState({
    bucketName: 'tree',
    cacheName: `conformation${capitalize(tableName)}`,
    bucketType: 'localStorage',
    defaultValue: undefined,
  });
  const conformation = deserializeConformation(rawConformation);

  function updateConformation(value: Conformations | undefined): void {
    if (typeof value === 'undefined') setConformation('');
    else {
      const encoded = serializeConformation(value);
      navigation.push(
        querystring.format(window.location.href, { conformation: encoded })
      );
      setConformation(encoded);
    }
  }

  React.useEffect(() => {
    const { conformation } = querystring.parse();
    if (typeof conformation === 'string' && conformation.length > 0)
      updateConformation(deserializeConformation(conformation));
  }, []);

  useTitle(treeText('treeViewTitle')(table.getLocalizedName()));

  // Node sort order
  const sortOrderFieldName = `${capitalize(tableName)}.treeview_sort_field`;
  const sortField = getPref(sortOrderFieldName, 'name');
  const baseUrl = `/api/specify_tree/${tableName}/${treeDefinition.id}`;
  const getRows = React.useCallback(
    async (parentId: number | 'null') =>
      fetchRows(`${baseUrl}/${parentId}/${sortField}`),
    [baseUrl, sortField]
  );

  const statsThreshold = getIntPref(
    `TreeEditor.Rank.Threshold.${capitalize(tableName)}`
  );
  const getStats = React.useCallback(
    async (nodeId: number | 'null', rankId: number): Promise<Stats> =>
      typeof statsThreshold === 'undefined' || statsThreshold > rankId
        ? Promise.resolve({})
        : fetchStats(`${baseUrl}/${nodeId}/stats/`),
    [baseUrl, statsThreshold]
  );

  const [rows, setRows] = React.useState<RA<Row> | undefined>(undefined);

  React.useEffect(() => {
    void getRows('null').then((rows) =>
      destructorCalled ? undefined : setRows(rows)
    );

    let destructorCalled = false;
    return (): void => {
      destructorCalled = true;
    };
  }, [getRows]);

  const id = useId('tree-view');

  return typeof rows === 'undefined' ? (
    <LoadingScreen />
  ) : (
    <section className={className.containerFull}>
      <header className="flex flex-wrap items-center gap-2">
        <h2>{table.getLocalizedName()}</h2>
        <Autocomplete
          source={async (value) => {
            const collection = new table.LazyCollection({
              filters: { name__istartswith: value, orderby: 'name' },
              domainfilter: true,
            });
            await collection.fetch();
            return Object.fromEntries(
              collection.models.map((node) => {
                const rankDefinition = treeDefinitionItems.find(
                  (rank) =>
                    rank.get<number>('rankid') === node.get<number>('rankid')
                );
                const rankName =
                  rankDefinition?.get<string | null>('title') ??
                  rankDefinition?.get<string>('name') ??
                  node.get<string>('name');
                return [
                  node.get<string>('fullname'),
                  { label: rankName, data: node },
                ];
              })
            );
          }}
          onChange={(_value, { data }): void => {
            // TODO: listen to "onChange"
            console.log(data);
          }}
          inputProps={{
            className: 'tree-search',
            placeholder: treeText('searchTreePlaceholder'),
            title: treeText('searchTreePlaceholder'),
            'aria-label': treeText('searchTreePlaceholder'),
          }}
        />
        <span className="flex-1 -ml-2" />
        <menu className="contents">
          <li className="contents">
            <Button.Simple disabled>{commonText('query')}</Button.Simple>
          </li>
          <li className="contents">
            <Button.Simple disabled>{commonText('edit')}</Button.Simple>
          </li>
          <li className="contents">
            <Button.Simple disabled>{commonText('addChild')}</Button.Simple>
          </li>
          <li className="contents">
            <Button.Simple disabled>{commonText('move')}</Button.Simple>
          </li>
          <li className="contents">
            <Button.Simple disabled>{treeText('merge')}</Button.Simple>
          </li>
          <li className="contents">
            <Button.Simple disabled>{treeText('synonymize')}</Button.Simple>
          </li>
        </menu>
      </header>
      <div
        className={`grid-table grid-cols-[repeat(var(--cols),auto)] flex-1
          overflow-auto bg-gray-200 shadow-md shadow-gray-500 content-start
          bg-gradient-to-bl from-[hsl(26deg_92%_62%_/_0)] rounded p-2 pt-0
          via-[hsl(26deg_92%_62%_/_20%)] to-[hsl(26deg_92%_62%_/_0)]`}
        style={{ '--cols': treeDefinitionItems.length } as React.CSSProperties}
        // First role is for screen readers. Second is for styling
        role="none table"
      >
        <div role="none rowgroup">
          <div role="none row">
            {treeDefinitionItems.map((rank, index, { length }) => (
              <div
                role="columnheader"
                key={index}
                className={`border whitespace-nowrap border-transparent top-0
                  sticky bg-gray-100/60 p-2 backdrop-blur-sm
                  ${index === 0 ? '-ml-2 pl-4 rounded-bl' : ''}
                  ${index + 1 === length ? 'pr-4 -mr-2 rounded-br' : ''}`}
              >
                <Button.LikeLink
                  id={id(rank.get<number>('rankId').toString())}
                  onClick={
                    typeof collapsedRanks === 'undefined'
                      ? undefined
                      : (): void =>
                          setCollapsedRanks(
                            collapsedRanks.includes(rank.get<number>('rankId'))
                              ? collapsedRanks.filter(
                                  (rankId) =>
                                    rankId !== rank.get<number>('rankId')
                                )
                              : [...collapsedRanks, rank.get<number>('rankId')]
                          )
                  }
                >
                  {pipe(
                    rank.get<string | null>('title') ??
                      rank.get<string>('name'),
                    collapsedRanks?.includes(rank.get<number>('rankId')) ??
                      false,
                    (name) => name[0]
                  )}
                </Button.LikeLink>
              </div>
            ))}
          </div>
        </div>
        <ul role="tree rowgroup">
          {rows.map((row) => (
            <TreeRow
              key={row.nodeId}
              row={row}
              getRows={getRows}
              getStats={getStats}
              nodeStats={undefined}
              path={[]}
              ranks={rankIds}
              rankNameId={id}
              collapsedRanks={collapsedRanks ?? []}
              conformation={
                conformation
                  ?.find(([id]) => id === row.nodeId)
                  ?.slice(1) as Conformations
              }
              onChangeConformation={(newConformation): void =>
                updateConformation([
                  ...(conformation?.filter(([id]) => id !== row.nodeId) ?? []),
                  ...(typeof newConformation === 'undefined'
                    ? []
                    : ([[row.nodeId, ...newConformation]] as const)),
                ])
              }
            />
          ))}
        </ul>
      </div>
    </section>
  );
}

function TreeRow({
  row,
  getRows,
  getStats,
  nodeStats,
  path,
  ranks,
  rankNameId,
  collapsedRanks,
  conformation,
  onChangeConformation: handleChangeConformation,
}: {
  readonly row: Row;
  readonly getRows: (parentId: number | 'null') => Promise<RA<Row>>;
  readonly getStats: (
    nodeId: number,
    rankId: number
  ) => Promise<Stats | undefined>;
  readonly nodeStats: Stats[number] | undefined;
  readonly path: RA<Row>;
  readonly ranks: RA<number>;
  readonly rankNameId: (suffix: string) => string;
  readonly collapsedRanks: RA<number>;
  readonly conformation: Conformations | undefined;
  readonly onChangeConformation: (
    conformation: Conformations | undefined
  ) => void;
}): JSX.Element {
  const [rows, setRows] = React.useState<RA<Row> | undefined>(undefined);
  const [childStats, setChildStats] = React.useState<Stats | undefined>(
    undefined
  );
  const previousConformation = React.useRef<Conformations | undefined>(
    undefined
  );

  const isExpanded = typeof conformation !== 'undefined';
  const isLoading = isExpanded && typeof rows === 'undefined';
  React.useEffect(() => {
    if (!isLoading) return undefined;

    void getRows(row.nodeId).then((rows) =>
      destructorCalled ? undefined : setRows(rows)
    );

    let destructorCalled = false;
    return (): void => {
      destructorCalled = true;
    };
  }, [isLoading, getRows, row]);

  const isLoadingStats = isExpanded && typeof childStats === 'undefined';
  React.useEffect(() => {
    if (!isLoadingStats) return undefined;

    void getStats(row.nodeId, row.rankId).then((stats) =>
      destructorCalled || typeof stats === 'undefined'
        ? undefined
        : setChildStats(stats)
    );

    let destructorCalled = false;
    return (): void => {
      destructorCalled = true;
    };
  }, [isLoadingStats, getStats, row]);

  const parentRankId = path.slice(-1)[0]?.rankId;
  const id = useId('tree-node');
  return (
    <li role="treeitem row">
      {ranks.map((rankId) => {
        if (row.rankId === rankId)
          return (
            <Button.LikeLink
              key={rankId}
              /*
               * Shift all node labels using margin and padding to align nicely
               * with borders of <span> cells
               */
              className={`border whitespace-nowrap border-transparent aria-handled
              -mb-[12px] -ml-[5px] mt-2
              ${typeof row.acceptedId === 'undefined' ? '' : 'text-red-500'}`}
              aria-pressed={isLoading ? 'mixed' : isExpanded}
              title={
                typeof row.acceptedId === 'undefined'
                  ? undefined
                  : `${treeText('acceptedName')} ${
                      row.acceptedName ?? row.acceptedId
                    }`
              }
              aria-controls={id('children')}
              onClick={(): void => {
                if (typeof conformation === 'undefined')
                  if (typeof previousConformation.current === 'undefined')
                    handleChangeConformation([]);
                  else handleChangeConformation(previousConformation.current);
                else {
                  previousConformation.current = conformation;
                  handleChangeConformation(undefined);
                }
              }}
              aria-describedby={rankNameId(rankId.toString())}
            >
              <span
                className="-mr-2"
                aria-label={
                  isLoading
                    ? commonText('loading')
                    : row.children === 0
                    ? treeText('leafNode')
                    : isExpanded
                    ? treeText('opened')
                    : treeText('closed')
                }
              >
                {isLoading
                  ? icons.clock
                  : row.children === 0
                  ? icons.blank
                  : isExpanded
                  ? icons.chevronDown
                  : icons.chevronRight}
              </span>
              <span
                className={collapsedRanks.includes(rankId) ? 'sr-only' : ''}
              >
                {row.name}
                {typeof nodeStats === 'object' && (
                  <span
                    title={`${treeText('directCollectionObjectCount')}: ${
                      nodeStats.directCount
                    }\n${treeText('indirectCollectionObjectCount')}: ${
                      nodeStats.childCount
                    }`}
                    aria-label={`${treeText('directCollectionObjectCount')}: ${
                      nodeStats.directCount
                    }. ${treeText('indirectCollectionObjectCount')}: ${
                      nodeStats.childCount
                    }`}
                  >
                    {`(${formatNumber(nodeStats.directCount)}, ${formatNumber(
                      nodeStats.childCount
                    )})`}
                  </span>
                )}
              </span>
            </Button.LikeLink>
          );
        else {
          const indexOfAncestor = path.findIndex(
            (node) => node.rankId === rankId
          );
          const currentNode = path[indexOfAncestor + 1];
          return (
            <span
              key={rankId}
              aria-hidden="true"
              className={`border border-dotted border-transparent
              pointer-events-none whitespace-nowrap
              ${
                // Add left border for empty cell before tree node
                indexOfAncestor !== -1 &&
                !(typeof currentNode !== 'undefined' && currentNode.isLastChild)
                  ? 'border-l-gray-500'
                  : ''
              }
              ${
                // Add a line from parent till child
                parentRankId <= rankId && rankId < row.rankId
                  ? 'border-b-gray-500'
                  : ''
              }`}
            />
          );
        }
      })}
      {isExpanded && typeof rows !== 'undefined' ? (
        <ul role="group row" id={id('children')}>
          {rows.map((childRow) => (
            <TreeRow
              key={childRow.nodeId}
              row={childRow}
              getRows={getRows}
              getStats={getStats}
              nodeStats={childStats?.[childRow.nodeId]}
              path={[...path, row]}
              ranks={ranks}
              rankNameId={rankNameId}
              collapsedRanks={collapsedRanks}
              conformation={
                conformation
                  ?.find(([id]) => id === childRow.nodeId)
                  ?.slice(1) as Conformations
              }
              onChangeConformation={(newConformation): void =>
                handleChangeConformation([
                  ...conformation.filter(([id]) => id !== childRow.nodeId),
                  ...(typeof newConformation === 'undefined'
                    ? []
                    : ([[childRow.nodeId, ...newConformation]] as const)),
                ])
              }
            />
          ))}
        </ul>
      ) : undefined}
    </li>
  );
}

export default createBackboneView(TreeView);
