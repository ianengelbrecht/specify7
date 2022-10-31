import React from 'react';

import { fetchCollection } from '../DataModel/collection';
import { commonText } from '../../localization/common';
import { formsText } from '../../localization/forms';
import { schema } from '../DataModel/schema';
import type { SpecifyModel } from '../DataModel/specifyModel';
import { Dialog } from '../Molecules/Dialog';
import { ProtectedTool } from '../Permissions/PermissionDenied';
import { Button } from '../Atoms/Button';
import { Input, Label } from '../Atoms/Form';
import { Link } from '../Atoms/Link';
import { useAsyncState } from '../../hooks/useAsyncState';
import { useBooleanState } from '../../hooks/useBooleanState';
import { usePref } from '../UserPreferences/usePref';
import { useCachedState } from '../../hooks/useCachedState';

export function Definition({
  model,
}: {
  readonly model: SpecifyModel;
}): JSX.Element {
  const [isOpen, handleOpen, handleClose] = useBooleanState();
  return (
    <>
      <Button.Small onClick={handleOpen}>
        {commonText('formDefinition')}
      </Button.Small>
      {isOpen && <FormDefinitionDialog model={model} onClose={handleClose} />}
    </>
  );
}

function FormDefinitionDialog({
  model,
  onClose: handleClose,
}: {
  readonly model: SpecifyModel;
  readonly onClose: () => void;
}): JSX.Element {
  return (
    <Dialog
      buttons={commonText('close')}
      header={commonText('formDefinition')}
      onClose={handleClose}
    >
      <UseAutoForm model={model} />
      <UseLabels />
      <EditFormDefinition />
    </Dialog>
  );
}

function UseAutoForm({ model }: { readonly model: SpecifyModel }): JSX.Element {
  const [globalConfig, setGlobalConfig] = usePref(
    'form',
    'preferences',
    'useCustomForm'
  );
  const useCustomForm = globalConfig[model.name] ?? true;
  const handleChange = (checked: boolean): void =>
    setGlobalConfig({ ...globalConfig, [model.name]: !checked });

  return (
    <Label.Inline>
      <Input.Checkbox checked={!useCustomForm} onValueChange={handleChange} />
      {formsText('useAutoGeneratedForm')}
    </Label.Inline>
  );
}

function UseLabels(): JSX.Element {
  const [useFieldLabels = true, setUseFieldLabels] = useCachedState(
    'forms',
    'useFieldLabels'
  );

  return (
    <Label.Inline>
      <Input.Checkbox
        checked={useFieldLabels}
        onValueChange={(checked): void => {
          setUseFieldLabels(checked);
          globalThis.location.reload();
        }}
      />
      {formsText('useFieldLabels')}
    </Label.Inline>
  );
}

function EditFormDefinition(): JSX.Element {
  const viewDefinitionLink = useFormDefinition();
  return (
    <ProtectedTool action="read" tool="resources">
      {typeof viewDefinitionLink === 'string' && (
        <Link.NewTab href={viewDefinitionLink}>
          {formsText('editFormDefinition')}
        </Link.NewTab>
      )}
    </ProtectedTool>
  );
}

/*
 * BUG: this assumes that the ViewSet for current collection was the one used
 *   to render this form. That is not always the case.
 */
function useFormDefinition(): string | undefined {
  const [url] = useAsyncState(
    React.useCallback(
      async () =>
        fetchCollection(
          'SpViewSetObj',
          {
            limit: 1,
          },
          {
            spAppResourceDir__Collection: schema.domainLevelIds.collection,
          }
        )
          .then(({ records }) => records[0]?.id)
          .then((id) =>
            typeof id === 'number'
              ? `/specify/resources/view-set/${id}/`
              : undefined
          ),
      []
    ),
    false
  );
  return url;
}
