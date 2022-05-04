/**
 * Schema Configuration
 */

import React from 'react';

import { fetchCollection } from '../../collection';
import type { SpLocaleContainer } from '../../datamodel';
import type { SerializedResource } from '../../datamodelutils';
import { fetchFormatters } from '../../dataobjformatters';
import { index } from '../../helpers';
import { commonText } from '../../localization/common';
import { parseUrl } from '../../querystring';
import { formatAggregators } from '../../schemaconfighelper';
import type { JavaType, RelationshipType } from '../../specifyfield';
import type { IR, RA } from '../../types';
import { fetchContext as fetchUiFormatters } from '../../uiformatters';
import { useAsyncState, useTitle } from '../hooks';
import type { UserTool } from '../main';
import { createBackboneView } from '../reactbackboneextend';
import type {
  DataObjectFormatter,
  NewSpLocaleItemString,
  SpLocaleItemString,
  UiFormatter,
} from '../schemaconfig';
import { SchemaConfig } from '../schemaconfig';
import { webLinks } from '../weblinkbutton';
import { useSchemaLanguages } from './language';

export type WithFetchedStrings = {
  readonly strings: {
    readonly desc: SpLocaleItemString | NewSpLocaleItemString;
    readonly name: SpLocaleItemString | NewSpLocaleItemString;
  };
};

export type WithTableInfo = {
  readonly dataModel: {
    readonly pickLists: IR<{
      readonly name: string;
      readonly isSystem: boolean;
    }>;
  };
};

export type WithFieldInfo = {
  readonly dataModel: {
    readonly length: number | undefined;
    readonly isReadOnly: boolean;
    readonly relatedModelName: string | undefined;
    readonly isRequired: boolean;
    readonly isRelationship: boolean;
    readonly type: JavaType | RelationshipType;
    readonly canChangeIsRequired: boolean;
  };
};

function SchemaConfigWrapper({
  onClose: handleClose,
}: {
  readonly onClose: () => void;
}): JSX.Element | null {
  const { language: defaultLanguage, table: defaultTable } = parseUrl();

  useTitle(commonText('schemaConfig'));
  const languages = useSchemaLanguages();
  const [tables] = useAsyncState<IR<SerializedResource<SpLocaleContainer>>>(
    React.useCallback(async () => {
      return fetchCollection('SpLocaleContainer', {
        limit: 0,
        domainFilter: true,
        schemaType: 0,
      }).then(({ records }) => index(records));
    }, []),
    true
  );

  const [formatters, setFormatters] = React.useState<
    IR<DataObjectFormatter> | undefined
  >(undefined);
  const [aggregators, setAggregators] = React.useState<
    IR<DataObjectFormatter> | undefined
  >(undefined);

  React.useEffect(() => {
    void fetchFormatters.then(({ formatters, aggregators }) => {
      if (destructorCalled) return undefined;
      setFormatters(formatAggregators(formatters));
      setAggregators(formatAggregators(aggregators));
      return undefined;
    });
    let destructorCalled = false;
    return (): void => {
      destructorCalled = true;
    };
  }, []);

  const [uiFormatters] = useAsyncState<RA<UiFormatter>>(
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
  );

  const [loadedWebLinks] = useAsyncState(
    React.useCallback(async () => webLinks, []),
    true
  );

  return typeof languages === 'undefined' ||
    typeof tables === 'undefined' ||
    typeof formatters === 'undefined' ||
    typeof aggregators === 'undefined' ||
    typeof loadedWebLinks === 'undefined' ||
    typeof uiFormatters === 'undefined' ? null : (
    <SchemaConfig
      languages={languages}
      tables={tables}
      defaultLanguage={defaultLanguage}
      defaultTable={Object.values(tables).find(
        ({ name }) => name === defaultTable
      )}
      webLinks={Object.keys(loadedWebLinks).map(
        (value) => [value, value] as const
      )}
      uiFormatters={uiFormatters}
      dataObjFormatters={formatters}
      dataObjAggregators={aggregators}
      onClose={handleClose}
      onSave={(language): void =>
        // Reload the page after schema changes
        window.location.assign(
          `/specify/task/schema-config/?language=${language}`
        )
      }
    />
  );
}

const View = createBackboneView(SchemaConfigWrapper);

export const userTool: UserTool = {
  task: 'schema-config',
  title: commonText('schemaConfig'),
  isOverlay: true,
  view: ({ onClose }) => new View({ onClose }),
  groupLabel: commonText('customization'),
};
