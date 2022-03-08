import React from 'react';

import { ajax } from '../ajax';
import type { SpQuery, Tables } from '../datamodel';
import type { AnySchema } from '../datamodelutils';
import { keysToLowerCase } from '../datamodelutils';
import type { SpecifyResource } from '../legacytypes';
import commonText from '../localization/common';
import queryText from '../localization/query';
import { fetchPickList } from '../picklistmixins';
import type { QueryField } from '../querybuilderutils';
import {
  addAuditLogFields,
  queryFieldsToFieldSpecs,
  sortTypes,
  unParseQueryFields,
} from '../querybuilderutils';
import type { QueryFieldSpec } from '../queryfieldspec';
import type { SpecifyModel } from '../specifymodel';
import type { RA } from '../types';
import { userInformation } from '../userinfo';
import { generateMappingPathPreview } from '../wbplanviewmappingpreview';
import { Button, ContainerBase } from './basic';
import { SortIndicator, TableIcon } from './common';
import { crash } from './errorboundary';
import { useAsyncState } from './hooks';
import { Dialog } from './modaldialog';
import { QueryResults } from './queryresults';
import { RecordSelector } from './recordselector';

function TableHeaderCell({
  fieldSpec,
  ariaLabel,
  sortConfig,
  onSortChange: handleSortChange,
}: {
  readonly fieldSpec: QueryFieldSpec | undefined;
  readonly ariaLabel?: string;
  readonly sortConfig: QueryField['sortType'];
  readonly onSortChange?: (sortType: QueryField['sortType']) => void;
}): JSX.Element {
  const tableName = fieldSpec?.getField()?.model.name;

  const content =
    typeof fieldSpec === 'object' ? (
      <>
        {tableName && <TableIcon tableName={tableName} />}
        {generateMappingPathPreview(
          fieldSpec.baseTable.name,
          fieldSpec.toMappingPath()
        )}
      </>
    ) : undefined;
  return (
    <div
      role="columnheader"
      className="w-full min-w-max bg-brand-100 dark:bg-brand-500 border-b
        border-gray-500 p-1 [inset-block-start:_0] sticky [z-index:2]"
      aria-label={ariaLabel}
    >
      {typeof handleSortChange === 'function' ? (
        <Button.LikeLink
          onClick={(): void =>
            handleSortChange?.(
              sortTypes[(sortTypes.indexOf(sortConfig) + 1) % sortTypes.length]
            )
          }
        >
          {content}
          {typeof sortConfig === 'string' && (
            <SortIndicator
              fieldName={'field'}
              sortConfig={{
                sortField: 'field',
                ascending: sortConfig === 'ascending',
              }}
            />
          )}
        </Button.LikeLink>
      ) : (
        content
      )}
    </div>
  );
}

function ViewRecords({
  model,
  results,
  selectedRows,
  onFetchMore: handleFetchMore,
}: {
  readonly model: SpecifyModel;
  readonly results: RA<RA<string | number | null>>;
  readonly selectedRows: Set<number>;
  readonly onFetchMore: (() => void) | undefined;
}): JSX.Element {
  const [isOpen, setIsOpen] = React.useState(false);
  const [records, setRecords] = React.useState<
    RA<SpecifyResource<AnySchema>> | undefined
  >(undefined);
  React.useEffect(() => {
    if (!isOpen) return;
    const ids =
      selectedRows.size === 0
        ? (results.map((row) => row[queryIdField]) as RA<number>)
        : Array.from(selectedRows);
    const indexedRecords = Object.fromEntries(
      records?.map((record) => [record.id, record]) ?? []
    );
    setRecords(
      ids.map((id) => indexedRecords[id] ?? new model.Resource({ id }))
    );
  }, [results, isOpen, records, model, selectedRows]);
  return (
    <>
      <Button.Simple
        onClick={(): void => setIsOpen(true)}
        disabled={results.length === 0}
      >
        {commonText('viewRecords')}
      </Button.Simple>
      <Dialog
        isOpen={isOpen}
        header={model.label}
        buttons={commonText('close')}
        onClose={(): void => setIsOpen(false)}
      >
        {typeof records === 'object' && (
          <RecordSelector
            model={model}
            isDependent={false}
            records={records}
            isReadOnly={userInformation.isReadOnly}
            hasHeader={false}
            onAdd={undefined}
            onSlide={(index): void =>
              index + 1 === records.length ? handleFetchMore?.() : undefined
            }
            onDelete={(index): void =>
              setRecords([
                ...records.slice(0, index),
                ...records.slice(index + 1),
              ])
            }
          />
        )}
      </Dialog>
    </>
  );
}

const threshold = 20;
const isScrolledBottom = (scrollable: HTMLElement): boolean =>
  scrollable.scrollHeight - scrollable.scrollTop - scrollable.clientHeight >
  threshold;

export function QueryResultsTable({
  model,
  label = queryText('results'),
  hasIdField,
  fetchResults,
  totalCount,
  fieldSpecs,
  initialData,
  sortConfig,
  onSortChange: handleSortChange,
}: {
  readonly model: SpecifyModel;
  readonly label?: string;
  readonly hasIdField: boolean;
  readonly fetchResults: (
    offset: number
  ) => Promise<RA<RA<string | number | null>>>;
  readonly totalCount: number;
  readonly fieldSpecs: RA<QueryFieldSpec>;
  readonly initialData: RA<RA<string | number | null>> | undefined;
  readonly sortConfig?: RA<QueryField['sortType']>;
  readonly onSortChange?: (
    fieldIndex: number,
    direction: 'ascending' | 'descending' | undefined
  ) => void;
}): JSX.Element {
  const [isFetching, setIsFetching] = React.useState(false);
  const [results, setResults] = React.useState<
    RA<RA<string | number | null>> | undefined
  >(initialData);
  React.useEffect(() => setResults(initialData), [initialData]);

  const [pickListsLoaded] = useAsyncState(
    React.useCallback(
      async () =>
        // Fetch all pick lists so that they are accessible synchronously later
        Promise.all(
          fieldSpecs
            .map((fieldSpec) => fieldSpec.getField()?.getPickList())
            .map((pickListName) =>
              typeof pickListName === 'string'
                ? fetchPickList(pickListName)
                : undefined
            )
        ).then(() => true),
      [fieldSpecs]
    )
  );

  const [selectedRows, setSelectedRows] = React.useState<Set<number>>(
    new Set()
  );
  const lastSelectedRow = React.useRef<number | undefined>(undefined);
  React.useEffect(() => setSelectedRows(new Set()), [totalCount]);
  const fetchMore = (): void =>
    Array.isArray(results)
      ? void fetchResults(results.length)
          .then((newResults) => setResults([...results, ...newResults]))
          .then(() => setIsFetching(false))
          .catch(crash)
      : undefined;

  return (
    <ContainerBase className="overflow-hidden">
      <div className="gap-x-2 flex items-center">
        <h3>{`${label}: (${totalCount})`}</h3>
        <div className="flex-1 -ml-2" />
        {hasIdField && Array.isArray(results) ? (
          <ViewRecords
            selectedRows={selectedRows}
            results={results}
            model={model}
            onFetchMore={isFetching ? undefined : fetchMore}
          />
        ) : undefined}
      </div>
      {Array.isArray(results) && fieldSpecs.length > 0 && pickListsLoaded && (
        <div
          role="table"
          className={`grid-table overflow-auto max-h-[75vh] border-b
             border-gray-500 auto-rows-min
            ${
              hasIdField
                ? `grid-cols-[min-content,min-content,repeat(var(--cols),auto)]`
                : `grid-cols-[repeat(var(--cols),auto)]`
            }`}
          style={{ '--cols': fieldSpecs.length } as React.CSSProperties}
          onScroll={
            isFetching || results.length === totalCount
              ? undefined
              : ({ target }): void => {
                  if (isScrolledBottom(target as HTMLElement)) return;
                  setIsFetching(true);
                  fetchMore();
                }
          }
        >
          <div role="rowgroup">
            <div role="row">
              {hasIdField && (
                <>
                  <TableHeaderCell
                    key="select-record"
                    fieldSpec={undefined}
                    ariaLabel={commonText('selectRecord')}
                    sortConfig={undefined}
                    onSortChange={undefined}
                  />
                  <TableHeaderCell
                    key="view-record"
                    fieldSpec={undefined}
                    ariaLabel={commonText('viewRecord')}
                    sortConfig={undefined}
                    onSortChange={undefined}
                  />
                </>
              )}
              {fieldSpecs.map((fieldSpec, index) => (
                <TableHeaderCell
                  key={index}
                  fieldSpec={fieldSpec}
                  sortConfig={sortConfig?.[index]}
                  onSortChange={
                    typeof handleSortChange === 'function'
                      ? (sortType): void => handleSortChange?.(index, sortType)
                      : undefined
                  }
                />
              ))}
            </div>
          </div>
          <QueryResults
            model={model}
            fieldSpecs={fieldSpecs}
            hasIdField={hasIdField}
            results={results}
            selectedRows={selectedRows}
            onSelected={(id, isSelected, isShiftClick): void => {
              if (hasIdField) return;
              const rowIndex = results.findIndex(
                (row) => row[queryIdField] === id
              );
              const ids = (
                isShiftClick && typeof lastSelectedRow.current === 'number'
                  ? Array.from(
                      {
                        length:
                          Math.abs(lastSelectedRow.current - rowIndex) + 1,
                      },
                      (_, index) =>
                        Math.min(lastSelectedRow.current!, rowIndex) + index
                    )
                  : [rowIndex]
              ).map((rowIndex) => results[rowIndex][queryIdField] as number);
              setSelectedRows(
                new Set([
                  ...Array.from(selectedRows).filter(
                    (id) => isSelected || !ids.includes(id)
                  ),
                  ...(isSelected ? ids : []),
                ])
              );
              lastSelectedRow.current = rowIndex;
            }}
          />
        </div>
      )}
      {isFetching && <QueryResultsLoading />}
    </ContainerBase>
  );
}

export function QueryResultsLoading(): JSX.Element {
  return (
    <img
      src="/static/img/specify128spinner.gif"
      alt={commonText('loading')}
      className="w-10"
      aria-live="polite"
    />
  );
}

/** Record ID column index in Query Results when not in distinct mode */
export const queryIdField = 0;

export function QueryResultsWrapper({
  baseTableName,
  model,
  queryRunCount,
  queryResource,
  fields,
  recordSetId,
  onSortChange: handleSortChange,
}: {
  readonly baseTableName: keyof Tables;
  readonly model: SpecifyModel;
  readonly queryRunCount: number;
  readonly queryResource: SpecifyResource<SpQuery>;
  readonly fields: RA<QueryField>;
  readonly recordSetId: number | undefined;
  readonly onSortChange?: (
    fieldIndex: number,
    direction: 'ascending' | 'descending' | undefined
  ) => void;
}): JSX.Element | null {
  const fetchResults = React.useCallback(
    async (offset: number) => {
      return ajax<{ readonly results: RA<RA<string | number | null>> }>(
        '/stored_query/ephemeral/',
        {
          method: 'POST',
          // eslint-disable-next-line @typescript-eslint/naming-convention
          headers: { Accept: 'application/json' },
          body: keysToLowerCase({
            ...queryResource.toJSON(),
            fields: unParseQueryFields(
              baseTableName,
              addAuditLogFields(baseTableName, fields),
              []
            ),
            recordSetId,
            limit: 40,
            offset,
          }),
        }
      ).then(({ data }) => data.results);
    },
    [fields, baseTableName, queryResource, recordSetId]
  );

  const [payload, setPayload] = React.useState<
    | {
        readonly fieldSpecs: RA<QueryFieldSpec>;
        readonly totalCount: number;
        readonly initialData: RA<RA<string | number | null>> | undefined;
      }
    | undefined
  >(undefined);
  React.useEffect(() => {
    if (queryRunCount === 0) return;
    setPayload(undefined);

    const allFields = addAuditLogFields(baseTableName, fields);

    const totalCount = ajax<{ readonly count: number }>(
      '/stored_query/ephemeral/',
      {
        method: 'POST',
        // eslint-disable-next-line @typescript-eslint/naming-convention
        headers: { Accept: 'application/json' },
        body: keysToLowerCase({
          ...queryResource.toJSON(),
          fields: unParseQueryFields(baseTableName, allFields, []),
          recordSetId,
          countOnly: true,
        }),
      }
    ).then(({ data }) => data.count);

    const displayedFields = allFields.filter((field) => field.isDisplay);
    const initialData =
      queryResource.get('countOnly') === true || displayedFields.length === 0
        ? undefined
        : fetchResults(0);
    const fieldSpecs = queryFieldsToFieldSpecs(
      baseTableName,
      displayedFields
    ).map(([_field, fieldSpec]) => fieldSpec);

    Promise.all([totalCount, initialData])
      .then(([totalCount, initialData]) =>
        setPayload({
          fieldSpecs,
          totalCount,
          initialData,
        })
      )
      .catch(crash);
  }, [
    fields,
    baseTableName,
    fetchResults,
    queryResource,
    queryRunCount,
    recordSetId,
  ]);

  return typeof payload === 'undefined' ? (
    queryRunCount === 0 ? null : (
      <QueryResultsLoading />
    )
  ) : (
    <QueryResultsTable
      model={model}
      hasIdField={queryResource.get('selectDistinct') !== true}
      fetchResults={fetchResults}
      totalCount={payload.totalCount}
      fieldSpecs={payload.fieldSpecs}
      initialData={payload.initialData}
      sortConfig={fields.map((field) => field.sortType)}
      onSortChange={handleSortChange}
    />
  );
}
