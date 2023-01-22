import type { LocalizedString } from 'typesafe-i18n';

import { f } from '../../utils/functools';
import type { SpecifyModel } from '../DataModel/specifyModel';
import type { SpecToJson } from '../Syncer';
import { pipe, syncer } from '../Syncer';
import { syncers } from '../Syncer/syncers';
import type { SimpleXmlNode } from '../Syncer/xmlToJson';
import { createSimpleXmlNode } from '../Syncer/xmlToJson';
import { createXmlSpec } from '../Syncer/xmlUtils';

export const formattersSpec = f.store(() =>
  createXmlSpec({
    formatters: pipe(
      syncers.xmlChildren('format'),
      syncers.map(
        pipe(
          syncers.object(formatterSpec()),
          syncers.dependent('definition', switchSpec),
          syncer(
            (formatter) => formatter,
            ({ definition, ...formatter }) => ({
              ...formatter,
              definition: {
                ...definition,
                isSingle: definition.fields.length <= 1,
              },
            })
          )
        )
      )
    ),
    aggregators: pipe(
      syncers.xmlChild('aggregators'),
      syncers.default<SimpleXmlNode>(() => createSimpleXmlNode('aggregators')),
      syncers.xmlChildren('aggregator'),
      syncers.map(
        pipe(
          syncers.object(aggregatorSpec()),
          syncer(
            ({ table, sortField, ...rest }) => ({
              ...rest,
              table,
              sortField: syncers.field(table?.name).serializer(sortField),
            }),
            ({ table, sortField, ...rest }) => ({
              ...rest,
              table,
              sortField: syncers.field(table?.name).deserializer(sortField),
            })
          )
        )
      )
    ),
  })
);

export type Formatter = SpecToJson<
  ReturnType<typeof formattersSpec>
>['formatters'][number];
export type Aggregator = SpecToJson<
  ReturnType<typeof formattersSpec>
>['aggregators'][number];

const formatterSpec = f.store(() =>
  createXmlSpec({
    name: pipe(
      syncers.xmlAttribute('name', 'required'),
      syncers.default<LocalizedString>('')
    ),
    title: syncers.xmlAttribute('title', 'empty'),
    table: pipe(
      syncers.xmlAttribute('class', 'required'),
      syncers.maybe(syncers.javaClassName)
    ),
    // FIXME: enforce single default in the UI
    isDefault: pipe(
      syncers.xmlAttribute('default', 'empty'),
      syncers.default<LocalizedString>(''),
      syncers.toBoolean
    ),
    definition: pipe(
      syncers.xmlChild('switch'),
      syncers.default<SimpleXmlNode>(() => createSimpleXmlNode('switch'))
    ),
  })
);

const switchSpec = ({ table }: SpecToJson<ReturnType<typeof formatterSpec>>) =>
  createXmlSpec({
    isSingle: pipe(
      syncers.xmlAttribute('single', 'skip'),
      syncers.maybe(syncers.toBoolean)
    ),
    conditionField: pipe(
      syncers.xmlAttribute('field', 'skip'),
      syncers.field(table?.name),
      syncer((fields) => {
        const field = fields?.at(-1);
        // FIXME: add validation for no -to-manys in the middle (and in forms too)
        if (field?.isRelationship === true && field.isDependent()) {
          console.error('Dependent relationship may not be used as condition');
          return undefined;
        } else return fields;
      }, f.id)
    ),
    external: syncers.xmlChild('external', 'optional'),
    fields: pipe(
      syncers.xmlChildren('fields'),
      syncers.map(syncers.object(fieldsSpec(table)))
    ),
  });

const fieldsSpec = (table: SpecifyModel | undefined) =>
  createXmlSpec({
    value: syncers.xmlAttribute('value', 'skip'),
    fields: pipe(
      syncers.xmlChildren('field'),
      syncers.map(
        pipe(
          syncers.object(fieldSpec(table)),
          syncers.change(
            'fieldFormatter',
            ({ field, fieldFormatter }) => {
              if (
                field?.at(-1)?.isRelationship === true &&
                typeof fieldFormatter === 'string'
              ) {
                console.warn(
                  'Field formatter is ignored for relationship fields'
                );
                return undefined;
              }
              return fieldFormatter;
            },
            ({ fieldFormatter }) => fieldFormatter
          ),
          syncers.change(
            'formatter',
            ({ field, formatter }) => {
              if (
                field?.at(-1)?.isRelationship === false &&
                typeof formatter === 'string'
              ) {
                console.warn(
                  'Record formatter is ignored for non-relationship fields'
                );
                return undefined;
              }
              return formatter;
            },
            ({ formatter }) => formatter
          )
        )
      )
    ),
  });

const fieldSpec = (table: SpecifyModel | undefined) =>
  createXmlSpec({
    separator: pipe(
      syncers.xmlAttribute('sep', 'skip', false),
      syncers.default<LocalizedString>('')
    ),
    aggregator: syncers.xmlAttribute('aggregator', 'skip'),
    formatter: syncers.xmlAttribute('formatter', 'skip'),
    fieldFormatter: syncers.xmlAttribute('uiFieldFormatter', 'skip'),
    field: pipe(syncers.xmlContent, syncers.field(table?.name)),
  });

const aggregatorSpec = f.store(() =>
  createXmlSpec({
    name: pipe(
      syncers.xmlAttribute('name', 'required'),
      syncers.default<LocalizedString>('')
    ),
    title: syncers.xmlAttribute('title', 'empty'),
    table: pipe(
      syncers.xmlAttribute('class', 'required'),
      syncers.maybe(syncers.javaClassName)
    ),
    isDefault: pipe(
      syncers.xmlAttribute('default', 'empty'),
      syncers.default<LocalizedString>(''),
      syncers.toBoolean
    ),
    separator: pipe(
      syncers.xmlAttribute('separator', 'empty', false),
      syncers.default<LocalizedString>('; ')
    ),
    suffix: syncers.xmlAttribute('ending', 'empty', false),
    limit: pipe(
      syncers.xmlAttribute('count', 'empty', false),
      syncers.default<LocalizedString>(''),
      syncers.toDecimal
    ),
    formatter: syncers.xmlAttribute('format', 'empty'),
    sortField: syncers.xmlAttribute('orderFieldName', 'empty'),
  })
);
