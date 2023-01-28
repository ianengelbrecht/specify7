import React from 'react';

import { deserializeResource } from '../../hooks/resource';
import { useCachedState } from '../../hooks/useCachedState';
import { treeText } from '../../localization/tree';
import type { RA, ValueOf } from '../../utils/types';
import { Button } from '../Atoms/Button';
import { className } from '../Atoms/className';
import { Form } from '../Atoms/Form';
import { icons } from '../Atoms/Icons';
import { serializeResource, specialFields } from '../DataModel/helpers';
import type { AnySchema, SerializedResource } from '../DataModel/helperTypes';
import type { SpecifyResource } from '../DataModel/legacyTypes';
import { resourceOn } from '../DataModel/resource';
import type { LiteralField, Relationship } from '../DataModel/specifyField';
import type { SpecifyModel } from '../DataModel/specifyModel';
import { FormField } from '../FormFields';
import type { FieldTypes } from '../FormParse/fields';
import { relationshipIsToMany } from '../WbPlanView/mappingHelpers';
import { resourceToGeneric } from './autoMerge';
import { MergeSubviewButton } from './CompareSubView';
import { MergeRow, MergingHeader } from './Header';
import { strictDependentFields } from '../FormMeta/CarryForward';

export function CompareRecords({
  formId,
  model,
  records,
  merged,
  onMerge: handleMerge,
  onDeleted: handleDeleted,
  onDismiss: handleDismiss,
}: {
  readonly formId: string;
  readonly model: SpecifyModel;
  readonly records: RA<SerializedResource<AnySchema>>;
  readonly merged: SpecifyResource<AnySchema>;
  readonly onMerge: (
    merged: SpecifyResource<AnySchema>,
    resources: RA<SpecifyResource<AnySchema>>
  ) => void;
  readonly onDeleted: (id: number) => void;
  readonly onDismiss: (id: number) => void;
}): JSX.Element {
  const resources = React.useMemo(
    () => records.map(deserializeResource),
    [records]
  );
  const conformation = useMergeConformation(model, resources);
  return (
    <MergeContainer
      id={formId}
      recordCount={records.length}
      onSubmit={(): void => handleMerge(merged, resources)}
    >
      <MergingHeader
        merged={merged}
        resources={resources}
        onDeleted={handleDeleted}
        onDismiss={handleDismiss}
      />
      <tbody>
        {conformation.map((field) => (
          <CompareField
            field={field}
            key={field.name}
            merged={merged}
            resources={resources}
          />
        ))}
      </tbody>
    </MergeContainer>
  );
}

export function MergeContainer({
  id,
  recordCount,
  children,
  onSubmit: handleSubmit,
}: {
  readonly id: string;
  readonly recordCount: number;
  readonly children: React.ReactNode;
  readonly onSubmit: () => void;
}): JSX.Element {
  return (
    <Form className="overflow-hidden" id={id} onSubmit={handleSubmit}>
      <table
        className={`
          grid-table
          grid-cols-[auto,repeat(var(--columns),minmax(15rem,1fr))]
          overflow-auto
          [&_:is(th,td)]:p-1
          [&_:is(td,th):nth-child(2)]:mr-1
          [&_:is(td,th):nth-child(2)]:border-r
          [&_:is(td,th):nth-child(2)]:border-gray-500
          [&_:is(td,th):nth-child(2)]:pr-2
        `}
        style={
          {
            '--columns': recordCount + 1,
          } as React.CSSProperties
        }
      >
        {children}
      </table>
    </Form>
  );
}

export function useMergeConformation(
  model: SpecifyModel,
  records: RA<SpecifyResource<AnySchema>>
): RA<LiteralField | Relationship> {
  const [showMatching = false] = useCachedState(
    'merging',
    'showMatchingFields'
  );
  return React.useMemo(() => {
    // Don't display independent -to-many relationships
    const fields = model.fields.filter(
      (field) =>
        !unMergeableFields.has(field.name) &&
        (!field.isRelationship ||
          field.isDependent() ||
          !relationshipIsToMany(field))
    );
    const differing = findDiffering(showMatching, fields, records);
    return showMatching ? differing : hideDependent(differing);
  }, [showMatching, model, records]);
}

export const unMergeableFields = new Set([
  ...specialFields,
  'timestampCreated',
  'timestampModified',
  'version',
]);

// FIXME: add tests
function findDiffering(
  showMatching: boolean,
  fields: RA<LiteralField | Relationship>,
  records: RA<SpecifyResource<AnySchema>>
): RA<LiteralField | Relationship> {
  if (records.length > 0 && !showMatching) {
    const filteredFields = fields
      .filter(
        (field) =>
          new Set(
            records
              .map((record) =>
                field.isRelationship && field.isDependent()
                  ? record.getDependentResource(field.name)?.toJSON()
                  : record.get(field.name)
              )
              .map((value) =>
                value === null ||
                value === undefined ||
                (Array.isArray(value) && value.length === 0)
                  ? ''
                  : value
              )
          ).size > 1
      )
      .filter(({ name }) => !unMergeableFields.has(name));
    /*
     * Even if user said to not show matching, show them anyway in cases where
     * all fields match. Otherwise, it won't show any fields at all which might
     * be more confusing
     */
    if (filteredFields.length > 0) return filteredFields;
  }
  const nonEmptyFields = fields.filter((field) =>
    records.some((record) => {
      const value =
        field.isRelationship && field.isDependent()
          ? record.getDependentResource(field.name)
          : (record.get(field.name) as string);
      return value !== undefined && value !== null && value !== '';
    })
  );
  return nonEmptyFields.length === 0 ? fields : nonEmptyFields;
}

// FIXME: add tests
/**
 * If date1 is already in the list of fields, don't also include date1precision
 * as merging date1 should also merge date1precision.
 */
const hideDependent = (
  fields: RA<LiteralField | Relationship>
): RA<LiteralField | Relationship> =>
  fields.filter(({ name }) => {
    const sourceField = strictDependentFields()[name];
    return (
      sourceField === undefined ||
      !fields.some(({ name }) => name === sourceField)
    );
  });

export function CompareField({
  field,
  resources,
  merged,
}: {
  readonly field: LiteralField | Relationship;
  readonly resources: RA<SpecifyResource<AnySchema> | undefined>;
  readonly merged: SpecifyResource<AnySchema> | undefined;
}): JSX.Element {
  return (
    <MergeRow header={field.label}>
      <Field
        field={field}
        isReadOnly={false}
        merged={undefined}
        resource={merged}
        resources={resources}
      />
      {resources.map((resource, index) => (
        <Field
          field={field}
          isReadOnly
          key={index}
          merged={merged}
          resource={resource}
          resources={resources}
        />
      ))}
    </MergeRow>
  );
}

function Field({
  field,
  resource,
  resources,
  merged,
  isReadOnly,
}: {
  readonly field: LiteralField | Relationship;
  readonly resource: SpecifyResource<AnySchema> | undefined;
  readonly resources: RA<SpecifyResource<AnySchema> | undefined>;
  readonly merged: SpecifyResource<AnySchema> | undefined;
  readonly isReadOnly: boolean;
}): JSX.Element {
  const fieldDefinition = React.useMemo(
    () => ({
      ...fieldToDefinition(field),
      isReadOnly: false,
    }),
    [field]
  );
  return resource === undefined ? (
    <td />
  ) : (
    <td className="!items-stretch">
      {typeof merged === 'object' && (
        <MergeButton field={field} from={resource} to={merged} />
      )}
      {!field.isRelationship ||
      (!field.isDependent() && !relationshipIsToMany(field)) ? (
        <div className="flex flex-1 items-center justify-center">
          <FormField
            fieldDefinition={fieldDefinition}
            fieldName={field.name}
            /*
             * Don't use auto grow text area, but do display query combo box
             * controls
             */
            formType={field.isRelationship ? 'form' : 'formTable'}
            id={undefined}
            isRequired={false}
            mode={isReadOnly || typeof merged === 'object' ? 'view' : 'edit'}
            resource={resource}
          />
        </div>
      ) : (
        <MergeSubviewButton
          merged={merged}
          relationship={field}
          resource={resource}
          resources={resources}
        />
      )}
    </td>
  );
}

function fieldToDefinition(
  field: LiteralField | Relationship
): ValueOf<FieldTypes> {
  if (field.isRelationship)
    return {
      type: 'QueryComboBox',
      hasCloneButton: false,
      typeSearch: undefined,
    };
  else if (field.type === 'java.lang.Boolean')
    return {
      type: 'Checkbox',
      defaultValue: undefined,
      label: undefined,
      printOnSave: false,
    };
  else if (field.type === 'text')
    return {
      type: 'TextArea',
      defaultValue: undefined,
      rows: undefined,
    };
  else if (typeof field.getPickList() === 'string')
    return {
      type: 'ComboBox',
      defaultValue: undefined,
      pickList: undefined,
    };
  else
    return {
      type: 'Text',
      defaultValue: undefined,
      min: undefined,
      max: undefined,
      step: undefined,
    };
}

export function MergeButton({
  field,
  from,
  to,
}: {
  readonly field: LiteralField | Relationship | undefined;
  readonly from: SpecifyResource<AnySchema>;
  readonly to: SpecifyResource<AnySchema>;
}): JSX.Element {
  const getValue = React.useCallback(
    (record: SpecifyResource<AnySchema>) =>
      field === undefined
        ? resourceToGeneric(serializeResource(record), true)
        : record.get(field.name),
    [field]
  );

  const [fromValue, setFromValue] = React.useState(() => getValue(from));
  React.useEffect(
    () => resourceOn(from, 'changed', () => setFromValue(getValue(from)), true),
    [from, field]
  );

  const [toValue, setToValue] = React.useState(() => getValue(to));
  React.useEffect(
    () => resourceOn(to, 'changed', () => setToValue(getValue(to)), true),
    [to, field]
  );

  const isSame = React.useMemo(
    () => JSON.stringify(fromValue) === JSON.stringify(toValue),
    [fromValue, toValue]
  );
  return (
    <Button.Small
      aria-label={treeText.merge()}
      disabled={isSame}
      title={treeText.merge()}
      variant={className.blueButton}
      onClick={(): void => {
        if (field === undefined)
          to.bulkSet(resourceToGeneric(serializeResource(from), false));
        else {
          const dependentFields = Object.entries(strictDependentFields())
            .filter(([_dependent, source]) => source === field.name)
            .map(([dependent]) => dependent);
          const allFields = [field.name, ...dependentFields];
          allFields.forEach((fieldName) =>
            to.set(fieldName, from.get(fieldName))
          );
        }
      }}
    >
      {icons.chevronLeft}
    </Button.Small>
  );
}
