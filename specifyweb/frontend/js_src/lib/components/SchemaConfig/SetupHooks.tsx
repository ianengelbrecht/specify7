import React from 'react';
import type { LocalizedString } from 'typesafe-i18n';

import { useAsyncState } from '../../hooks/useAsyncState';
import type { IR, RA } from '../../utils/types';
import { filterArray } from '../../utils/types';
import { index } from '../../utils/utils';
import { fetchCollection } from '../DataModel/collection';
import { serializeResource } from '../DataModel/helpers';
import type { SerializedResource } from '../DataModel/helperTypes';
import type { SpLocaleContainer } from '../DataModel/types';
import { webLinks } from '../FormPlugins/WebLink';
import { fetchFormatters } from '../Forms/dataObjFormatters';
import { fetchContext as fetchUiFormatters } from '../Forms/uiFormatters';
import { fetchPickLists } from '../PickLists/definitions';
import { useSchemaLanguages } from '../Toolbar/Language';
import { formatAggregators } from './helpers';

export type SchemaData = {
  readonly languages: IR<LocalizedString>;
  readonly tables: IR<SerializedResource<SpLocaleContainer>>;
  readonly formatters: IR<DataObjectFormatter>;
  readonly aggregators: IR<DataObjectFormatter>;
  readonly uiFormatters: RA<UiFormatter>;
  readonly webLinks: RA<readonly [string, string]>;
  readonly pickLists: IR<{
    readonly name: string;
    readonly isSystem: boolean;
  }>;
};

export type DataObjectFormatter = {
  readonly title: LocalizedString;
  readonly className: string;
};

type UiFormatter = {
  readonly name: string;
  readonly isSystem: boolean;
  readonly value: string;
};

export function useSchemaData(): SchemaData | undefined {
  const languages = useSchemaLanguages(true);
  const tables = useLocaleContainers();
  const formatters = useFormatters();
  const aggregators = useAggregators();
  const uiFormatters = useUiFormatters();
  const webLinks = useWebLinks();
  const pickLists = usePickLists();
  return languages === undefined ||
    tables === undefined ||
    formatters === undefined ||
    aggregators === undefined ||
    uiFormatters === undefined ||
    webLinks === undefined ||
    pickLists === undefined
    ? undefined
    : {
        languages,
        tables,
        formatters,
        aggregators,
        uiFormatters,
        webLinks,
        pickLists,
      };
}

function useLocaleContainers():
  | IR<SerializedResource<SpLocaleContainer>>
  | undefined {
  return useAsyncState<IR<SerializedResource<SpLocaleContainer>>>(
    React.useCallback(
      async () =>
        fetchCollection('SpLocaleContainer', {
          limit: 0,
          domainFilter: true,
          schemaType: 0,
        }).then(({ records }) => index(records)),
      []
    ),
    true
  )[0];
}

function useUiFormatters(): RA<UiFormatter> | undefined {
  return useAsyncState<RA<UiFormatter>>(
    React.useCallback(
      async () =>
        fetchUiFormatters.then((formatters) =>
          Object.entries(formatters)
            .map(([name, formatter]) => ({
              name,
              isSystem: formatter.isSystem,
              value: formatter.valueOrWild(),
            }))
            .filter(({ value }) => value)
        ),
      []
    ),
    true
  )[0];
}

function useFormatters(): IR<DataObjectFormatter> | undefined {
  return useAsyncState<IR<DataObjectFormatter>>(
    React.useCallback(
      async () =>
        fetchFormatters.then(({ formatters }) => formatAggregators(formatters)),
      []
    ),
    true
  )[0];
}

function useAggregators(): IR<DataObjectFormatter> | undefined {
  return useAsyncState<IR<DataObjectFormatter>>(
    React.useCallback(
      async () =>
        fetchFormatters.then(({ aggregators }) =>
          formatAggregators(aggregators)
        ),
      []
    ),
    true
  )[0];
}

function useWebLinks(): RA<readonly [string, string]> | undefined {
  return useAsyncState(
    React.useCallback(
      async () =>
        webLinks.then((webLinks) =>
          Object.keys(webLinks).map((value) => [value, value] as const)
        ),
      []
    ),
    true
  )[0];
}

function usePickLists():
  | IR<{
      readonly name: string;
      readonly isSystem: boolean;
    }>
  | undefined {
  return useAsyncState<
    IR<{
      readonly name: string;
      readonly isSystem: boolean;
    }>
  >(
    React.useCallback(
      async () =>
        fetchPickLists().then((pickLists) =>
          Object.fromEntries(
            filterArray(Object.values(pickLists))
              .map(serializeResource)
              .map(({ id, name, isSystem }) => [
                id,
                {
                  name,
                  isSystem,
                },
                // Filter out front-end only pick lists
              ])
              .filter(([id]) => typeof id === 'number')
          )
        ),
      []
    ),
    true
  )[0];
}
