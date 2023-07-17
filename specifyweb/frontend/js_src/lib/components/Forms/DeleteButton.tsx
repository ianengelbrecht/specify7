import React from 'react';

import { useAsyncState } from '../../hooks/useAsyncState';
import { useBooleanState } from '../../hooks/useBooleanState';
import { useLiveState } from '../../hooks/useLiveState';
import { commonText } from '../../localization/common';
import { formsText } from '../../localization/forms';
import { treeText } from '../../localization/tree';
import { StringToJsx } from '../../localization/utils';
import { ajax } from '../../utils/ajax';
import type { RA } from '../../utils/types';
import { overwriteReadOnly } from '../../utils/types';
import { Button } from '../Atoms/Button';
import { icons } from '../Atoms/Icons';
import { LoadingContext } from '../Core/Contexts';
import type { AnySchema } from '../DataModel/helperTypes';
import type { SpecifyResource } from '../DataModel/legacyTypes';
import { strictGetModel } from '../DataModel/schema';
import type { Tables } from '../DataModel/types';
import { loadingBar } from '../Molecules';
import { Dialog, dialogClassNames } from '../Molecules/Dialog';
import { FormattedResource } from '../Molecules/FormattedResource';
import { TableIcon } from '../Molecules/TableIcon';
import type { DeleteBlocker } from './DeleteBlocked';
import { DeleteBlocked } from './DeleteBlocked';

const fetchBlockers = async (
  resource: SpecifyResource<AnySchema>
): Promise<RA<DeleteBlocker>> =>
  ajax<
    RA<{
      readonly table: keyof Tables;
      readonly field: string;
      readonly id: number;
    }>
  >(
    `/api/delete_blockers/${resource.specifyModel.name.toLowerCase()}/${
      resource.id
    }/`,
    {
      // eslint-disable-next-line @typescript-eslint/naming-convention
      headers: { Accept: 'application/json' },
    }
  ).then(({ data }) =>
    data.map(({ table, ...rest }) => ({
      ...rest,
      model: strictGetModel(table),
    }))
  );

/**
 * A button to delele a resorce
 * Prompts before deletion
 * Checks for delete blockers (other resources depending on this one) before
 * deletion
 */
export function DeleteButton<SCHEMA extends AnySchema>({
  resource,
  deletionMessage = formsText.deleteConfirmationDescription(),
  deferred: initialDeferred = false,
  component: ButtonComponent = Button.Secondary,
  onDeleted: handleDeleted,
}: {
  readonly resource: SpecifyResource<SCHEMA>;
  readonly deletionMessage?: React.ReactNode;
  /**
   * As a performance optimization, can defer checking for delete blockers
   * until the button is clicked. This is used in the tree viewer as delete
   * button's resource can change often.
   */
  readonly deferred?: boolean;
  readonly component?: typeof Button['Secondary'];
  readonly onDeleted?: () => void;
}): JSX.Element {
  const [deferred, setDeferred] = useLiveState<boolean>(
    React.useCallback(() => initialDeferred, [initialDeferred, resource])
  );
  const [blockers, setBlockers] = useAsyncState<RA<DeleteBlocker>>(
    React.useCallback(
      async () => (deferred ? undefined : fetchBlockers(resource)),
      [resource, deferred]
    ),
    false
  );

  const [isOpen, handleOpen, handleClose] = useBooleanState();
  const loading = React.useContext(LoadingContext);

  const isBlocked = Array.isArray(blockers) && blockers.length > 0;

  const iconName = resource.specifyModel.name;

  return (
    <>
      <ButtonComponent
        title={isBlocked ? formsText.deleteBlocked() : undefined}
        onClick={(): void => {
          handleOpen();
          setDeferred(false);
        }}
      >
        {isBlocked ? icons.exclamation : undefined}
        {commonText.delete()}
      </ButtonComponent>
      {isOpen ? (
        blockers === undefined ? (
          <Dialog
            buttons={commonText.cancel()}
            className={{ container: dialogClassNames.narrowContainer }}
            header={commonText.loading()}
            onClose={handleClose}
          >
            {formsText.checkingIfResourceCanBeDeleted()}
            {loadingBar}
          </Dialog>
        ) : blockers.length === 0 ? (
          <Dialog
            buttons={
              <>
                <Button.Danger
                  onClick={(): void => {
                    /*
                     * REFACTOR: move this into ResourceApi.js
                     */
                    overwriteReadOnly(resource, 'needsSaved', false);
                    loading(resource.destroy().then(handleDeleted));
                  }}
                >
                  {commonText.delete()}
                </Button.Danger>
                <span className="-ml-2 flex-1" />
                <Button.DialogClose>{commonText.cancel()}</Button.DialogClose>
              </>
            }
            className={{
              container: dialogClassNames.narrowContainer,
            }}
            header={formsText.deleteConfirmation({
              tableName: resource.specifyModel.label,
            })}
            onClose={handleClose}
          >
            {deletionMessage}
            <div>
              <StringToJsx
                components={{
                  wrap: (
                    <i className="flex items-center gap-2">
                      <TableIcon label={false} name={iconName} />
                      <FormattedResource asLink={false} resource={resource} />
                    </i>
                  ),
                }}
                string={commonText.jsxColonLine({
                  label: treeText.resourceToDelete(),
                })}
              />
            </div>
          </Dialog>
        ) : (
          <DeleteBlocked
            blockers={blockers}
            resource={resource}
            onClose={handleClose}
            onDeleted={(): void => setBlockers([])}
          />
        )
      ) : undefined}
    </>
  );
}
