import React from 'react';

import { useBooleanState } from '../../hooks/useBooleanState';
import { useCachedState } from '../../hooks/useCachedState';
import { commonText } from '../../localization/common';
import { formsText } from '../../localization/forms';
import { Button } from '../Atoms/Button';
import { Input, Label } from '../Atoms/Form';
import { Link } from '../Atoms/Link';
import type { SpecifyModel } from '../DataModel/specifyModel';
import type { ViewDescription } from '../FormParse';
import { Dialog } from '../Molecules/Dialog';
import { ProtectedTool } from '../Permissions/PermissionDenied';
import { usePref } from '../UserPreferences/usePref';

export function Definition({
  model,
  viewDescription,
}: {
  readonly model: SpecifyModel;
  readonly viewDescription: ViewDescription | undefined;
}): JSX.Element {
  const [isOpen, handleOpen, handleClose] = useBooleanState();
  return (
    <>
      <Button.Small onClick={handleOpen}>
        {commonText('formDefinition')}
      </Button.Small>
      {isOpen && (
        <FormDefinitionDialog
          model={model}
          viewDescription={viewDescription}
          onClose={handleClose}
        />
      )}
    </>
  );
}

function FormDefinitionDialog({
  model,
  viewDescription,
  onClose: handleClose,
}: {
  readonly model: SpecifyModel;
  readonly viewDescription: ViewDescription | undefined;
  readonly onClose: () => void;
}): JSX.Element {
  const viewSetId = viewDescription?.viewSetId;
  return (
    <Dialog
      buttons={commonText('close')}
      header={commonText('formDefinition')}
      onClose={handleClose}
    >
      <UseAutoForm model={model} />
      <UseLabels />
      {typeof viewSetId === 'number' && (
        <EditFormDefinition viewSetId={viewSetId} />
      )}
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

  const initialValue = React.useRef(useFieldLabels);
  const isChanged = React.useRef(false);
  React.useEffect(() => {
    isChanged.current = useFieldLabels !== initialValue.current;
  }, [useFieldLabels]);

  React.useEffect(
    () => () => {
      if (isChanged.current) {
        globalThis.location.reload();
      }
    },
    []
  );

  return (
    <Label.Inline>
      <Input.Checkbox
        checked={useFieldLabels}
        onValueChange={setUseFieldLabels}
      />
      {formsText('useFieldLabels')}
    </Label.Inline>
  );
}

function EditFormDefinition({
  viewSetId,
}: {
  readonly viewSetId: number;
}): JSX.Element {
  return (
    <ProtectedTool action="read" tool="resources">
      <Link.NewTab href={`/specify/resources/view-set/${viewSetId}/`}>
        {formsText('editFormDefinition')}
      </Link.NewTab>
    </ProtectedTool>
  );
}
