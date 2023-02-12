import React from 'react';
import type { LocalizedString } from 'typesafe-i18n';

import { useAsyncState } from '../../hooks/useAsyncState';
import { useBooleanState } from '../../hooks/useBooleanState';
import { useId } from '../../hooks/useId';
import { commonText } from '../../localization/common';
import { formsText } from '../../localization/forms';
import { queryText } from '../../localization/query';
import { queryCbxExtendedSearch } from '../../utils/ajax/specifyApi';
import { f } from '../../utils/functools';
import type { RA } from '../../utils/types';
import { sortFunction } from '../../utils/utils';
import { Ul } from '../Atoms';
import { Button } from '../Atoms/Button';
import { Form } from '../Atoms/Form';
import { Link } from '../Atoms/Link';
import { Submit } from '../Atoms/Submit';
import type { AnySchema, CommonFields } from '../DataModel/helperTypes';
import type { SpecifyResource } from '../DataModel/legacyTypes';
import { getResourceViewUrl } from '../DataModel/resource';
import type { SpecifyModel } from '../DataModel/specifyModel';
import type { SpQueryField } from '../DataModel/types';
import { error } from '../Errors/assert';
import { raise } from '../Errors/Crash';
import { format } from '../Formatters/formatters';
import { RenderForm } from '../Forms/SpecifyForm';
import { useViewDefinition } from '../Forms/useViewDefinition';
import { load } from '../InitialContext';
import { Dialog, dialogClassNames } from '../Molecules/Dialog';
import { ProtectedAction } from '../Permissions/PermissionDenied';
import { createQuery } from '../QueryBuilder';
import type { QueryFieldFilter } from '../QueryBuilder/FieldFilter';
import { queryFieldFilters } from '../QueryBuilder/FieldFilter';
import { QueryFieldSpec } from '../QueryBuilder/fieldSpec';
import { QueryBuilder } from '../QueryBuilder/Wrapped';
import { formatUrl } from '../Router/queryString';
import { xmlToSpec } from '../Syncer/xmlUtils';
import { dialogsSpec } from './spec';

export const searchDialogDefinitions = f
  .all({
    xml: load<Element>(
      formatUrl('/context/app.resource', { name: 'DialogDefs' }),
      'text/xml'
    ),
    schema: import('../DataModel/schema').then(
      async ({ fetchContext }) => fetchContext
    ),
  })
  .then(({ xml }) => xmlToSpec(xml, dialogsSpec()).dialogs);

const resourceLimit = 100;

export type QueryComboBoxFilter<SCHEMA extends AnySchema> = {
  readonly field: string & (keyof CommonFields | keyof SCHEMA['fields']);
  readonly isNot: boolean;
  readonly operation: QueryFieldFilter & ('between' | 'in' | 'less');
  readonly value: string;
};

/**
 * Display a resource search dialog
 */
export function SearchDialog<SCHEMA extends AnySchema>({
  forceCollection,
  extraFilters = [],
  templateResource,
  multiple,
  onSelected: handleSelected,
  onClose: handleClose,
}: {
  readonly forceCollection: number | undefined;
  readonly extraFilters: RA<QueryComboBoxFilter<SCHEMA>> | undefined;
  readonly templateResource: SpecifyResource<SCHEMA>;
  readonly multiple: boolean;
  readonly onClose: () => void;
  readonly onSelected: (resources: RA<SpecifyResource<SCHEMA>>) => void;
}): JSX.Element | null {
  const [viewName, setViewName] = useAsyncState(
    React.useCallback(
      async () =>
        searchDialogDefinitions.then(
          (definitions) =>
            definitions.find(
              ({ type, name }) =>
                type === 'search' &&
                name.toLowerCase() ===
                  templateResource.specifyModel.searchDialog?.toLowerCase()
            )?.view ?? false
        ),
      [templateResource]
    ),
    true
  );

  const viewDefinition = useViewDefinition({
    model:
      typeof viewName === 'string' ? templateResource.specifyModel : undefined,
    viewName: typeof viewName === 'string' ? viewName : undefined,
    fallbackViewName: templateResource.specifyModel.view,
    formType: 'form',
    mode: 'search',
  });

  const [isLoading, handleLoading, handleLoaded] = useBooleanState();
  const [results, setResults] = React.useState<
    | RA<{
        readonly id: number;
        readonly formatted: LocalizedString;
        readonly resource: SpecifyResource<SCHEMA>;
      }>
    | undefined
  >(undefined);
  const id = useId('search-dialog');
  return typeof viewName === 'string' ? (
    <Dialog
      buttons={
        <>
          <Button.DialogClose>{commonText.cancel()}</Button.DialogClose>
          <ProtectedAction action="execute" resource="/querybuilder/query">
            <Button.Blue onClick={(): void => setViewName(false)}>
              {queryText.queryBuilder()}
            </Button.Blue>
          </ProtectedAction>
          <Submit.Green form={id('form')}>{commonText.search()}</Submit.Green>
        </>
      }
      header={commonText.search()}
      modal={false}
      onClose={handleClose}
    >
      <Form
        id={id('form')}
        onSubmit={(): void => {
          handleLoading();
          queryCbxExtendedSearch(templateResource, forceCollection)
            .then(async (resources) =>
              Promise.all(
                filterResults(resources, extraFilters).map(
                  async (resource) => ({
                    id: resource.id,
                    formatted: await format(resource, undefined, true),
                    resource,
                  })
                )
              ).then((results) =>
                setResults(
                  results.sort(sortFunction(({ formatted }) => formatted))
                )
              )
            )
            .finally(handleLoaded)
            .catch(raise);
        }}
      >
        <RenderForm
          display="inline"
          resource={templateResource}
          viewDefinition={viewDefinition}
        />
        <Ul
          className={`
            min-w-96 h-40 overflow-auto rounded
            border bg-white p-2 ring-1 ring-gray-500 dark:bg-neutral-700 dark:ring-0
          `}
        >
          {isLoading ? (
            <li>{commonText.loading()}</li>
          ) : results === undefined ? undefined : results.length === 0 ? (
            <li>{commonText.noResults()}</li>
          ) : (
            <>
              {results.map(({ id, formatted, resource }) => (
                <li key={id}>
                  <Link.Default
                    href={getResourceViewUrl(
                      templateResource.specifyModel.name,
                      id
                    )}
                    onClick={(event): void => {
                      event.preventDefault();
                      handleSelected([resource]);
                      handleClose();
                    }}
                  >
                    {formatted}
                  </Link.Default>
                </li>
              ))}
              {results.length === resourceLimit && (
                <li>
                  <span className="sr-only">
                    {formsText.additionalResultsOmitted()}
                  </span>
                  ...
                </li>
              )}
            </>
          )}
        </Ul>
      </Form>
    </Dialog>
  ) : viewName === false ? (
    <QueryBuilderSearch
      extraFilters={extraFilters}
      forceCollection={forceCollection}
      model={templateResource.specifyModel}
      multiple={multiple}
      onClose={handleClose}
      onSelected={(records): void => {
        handleSelected(records);
        handleClose();
      }}
    />
  ) : null;
}

const filterResults = <SCHEMA extends AnySchema>(
  results: RA<SpecifyResource<SCHEMA>>,
  extraFilters: RA<QueryComboBoxFilter<SCHEMA>>
): RA<SpecifyResource<SCHEMA>> =>
  results.filter((result) =>
    extraFilters.every((filter) => testFilter(result, filter))
  );

function testFilter<SCHEMA extends AnySchema>(
  resource: SpecifyResource<SCHEMA>,
  { operation, field, value, isNot }: QueryComboBoxFilter<SCHEMA>
): boolean {
  const values = value.split(',').map(f.trim);
  const result =
    operation === 'between'
      ? (resource.get(field) ?? 0) >= values[0] &&
        (resource.get(field) ?? 0) <= values[1]
      : operation === 'in'
      ? values.some(f.equal(resource.get(field)))
      : operation === 'less'
      ? values.every((value) => (resource.get(field) ?? 0) < value)
      : error('Invalid Query Combo Box search filter', {
          filter: {
            operation,
            field,
            values,
          },
          resource,
        });
  return isNot ? !result : result;
}

function QueryBuilderSearch<SCHEMA extends AnySchema>({
  forceCollection,
  extraFilters,
  model,
  onSelected: handleSelected,
  onClose: handleClose,
  multiple,
}: {
  readonly forceCollection: number | undefined;
  readonly extraFilters: RA<QueryComboBoxFilter<SCHEMA>>;
  readonly model: SpecifyModel<SCHEMA>;
  readonly onClose: () => void;
  readonly onSelected: (resources: RA<SpecifyResource<SCHEMA>>) => void;
  readonly multiple: boolean;
}): JSX.Element {
  const query = React.useMemo(
    () =>
      createQuery(commonText.search(), model).set(
        'fields',
        toQueryFields(model, extraFilters)
      ),
    [model, extraFilters]
  );
  const [selected, setSelected] = React.useState<RA<number>>([]);
  return (
    <Dialog
      buttons={
        <>
          <Button.DialogClose>{commonText.close()}</Button.DialogClose>
          <Button.Blue
            disabled={
              selected.length === 0 || (selected.length > 1 && !multiple)
            }
            onClick={(): void =>
              handleSelected(selected.map((id) => new model.Resource({ id })))
            }
          >
            {commonText.select()}
          </Button.Blue>
        </>
      }
      className={{
        container: dialogClassNames.wideContainer,
      }}
      header={queryText.queryBuilder()}
      onClose={handleClose}
    >
      <QueryBuilder
        forceCollection={forceCollection}
        isEmbedded
        isReadOnly={false}
        query={query}
        recordSet={undefined}
        onSelected={setSelected}
      />
    </Dialog>
  );
}

const toQueryFields = <SCHEMA extends AnySchema>(
  model: SpecifyModel<SCHEMA>,
  filters: RA<QueryComboBoxFilter<SCHEMA>>
): RA<SpecifyResource<SpQueryField>> =>
  filters.map(({ field, operation, isNot, value }) =>
    QueryFieldSpec.fromPath(model.name, [field])
      .toSpQueryField()
      .set('operStart', queryFieldFilters[operation].id)
      .set('isNot', isNot)
      .set('startValue', value)
  );
