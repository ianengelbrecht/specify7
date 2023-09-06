import React from 'react';

import { useBooleanState } from '../../hooks/useBooleanState';
import { useIsModified } from '../../hooks/useIsModified';
import { attachmentsText } from '../../localization/attachments';
import { commonText } from '../../localization/common';
import type { GetSet } from '../../utils/types';
import { Button } from '../Atoms/Button';
import { Form } from '../Atoms/Form';
import { icons } from '../Atoms/Icons';
import { deserializeResource, serializeResource } from '../DataModel/helpers';
import type { AnySchema, SerializedResource } from '../DataModel/helperTypes';
import type { SpecifyResource } from '../DataModel/legacyTypes';
import { schema } from '../DataModel/schema';
import type { SpecifyModel } from '../DataModel/specifyModel';
import type { Attachment } from '../DataModel/types';
import { SaveButton } from '../Forms/Save';
import { Dialog } from '../Molecules/Dialog';
import { getIIIFUrlFromVersion, IIIFViewer, useIIIFSpec } from './IIIFViewer';
import { AttachmentViewer } from './Viewer';

export function AttachmentDialog({
  attachment,
  related,
  onClose: handleClose,
  onChange: handleChange,
  onPrevious: handlePrevious,
  onNext: handleNext,
  onViewRecord: handleViewRecord,
}: {
  readonly attachment: SerializedResource<Attachment>;
  readonly related: GetSet<SpecifyResource<AnySchema> | undefined>;
  readonly onClose: () => void;
  readonly onChange: (attachment: SerializedResource<Attachment>) => void;
  readonly onPrevious: (() => void) | undefined;
  readonly onNext: (() => void) | undefined;
  readonly onViewRecord: (model: SpecifyModel, recordId: number) => void;
}): JSX.Element {
  const resource = React.useMemo(
    () => deserializeResource(attachment),
    [attachment]
  );

  const [form, setForm] = React.useState<HTMLFormElement | null>(null);

  const isModified = useIsModified(resource);

  const [showMeta, _, __, toggleShowMeta] = useBooleanState(true);

  // eslint-disable-next-line @typescript-eslint/naming-convention
  const validIIIFs = useIIIFSpec(resource.get('attachmentLocation'));

  const [activeIiifVersion, setActiveIiifVersion] = React.useState<
    number | undefined
  >(undefined);

  const latestIiifSupported = React.useMemo(
    () =>
      validIIIFs !== undefined && validIIIFs.length > 0
        ? validIIIFs.at(-1)
        : undefined,
    [validIIIFs]
  );
  return (
    <Dialog
      buttons={
        <>
          {isModified ? (
            <Button.Danger onClick={handleClose}>
              {commonText.cancel()}
            </Button.Danger>
          ) : (
            <Button.Info onClick={handleClose}>
              {commonText.close()}
            </Button.Info>
          )}
          {form !== null && (
            <SaveButton
              form={form}
              resource={resource}
              onAdd={undefined}
              onSaved={(): void => {
                handleChange(serializeResource(resource));
                handleClose();
              }}
            />
          )}
        </>
      }
      dimensionsKey="AttachmentViewer"
      header={
        attachment.title ??
        attachment.origFilename ??
        schema.models.Attachment.label
      }
      headerButtons={
        <>
          <span className="-ml-4 flex-1" />
          <Button.Info onClick={toggleShowMeta}>
            {showMeta ? attachmentsText.hideForm() : attachmentsText.showForm()}
          </Button.Info>
          {latestIiifSupported === undefined ? null : (
            <Button.Info
              className={
                activeIiifVersion === latestIiifSupported
                  ? 'brightness-200'
                  : ''
              }
              key={latestIiifSupported}
              onClick={(): void => setActiveIiifVersion(latestIiifSupported)}
            >
              {attachmentsText.viewIiif({
                version: latestIiifSupported.toString(),
              })}
            </Button.Info>
          )}
          {activeIiifVersion === undefined ? null : (
            <Button.Info onClick={(): void => setActiveIiifVersion(undefined)}>
              {attachmentsText.exitIiif()}
            </Button.Info>
          )}
        </>
      }
      icon={icons.photos}
      onClose={handleClose}
    >
      {activeIiifVersion === undefined ? (
        <div className="flex h-full gap-4">
          {/* FEATURE: keyboard navigation support */}
          <Button.Icon
            className="p-4"
            icon="chevronLeft"
            title={commonText.previous()}
            onClick={handlePrevious}
          />
          <Form className="flex-1" forwardRef={setForm}>
            <AttachmentViewer
              attachment={resource}
              related={related}
              showMeta={showMeta}
              onViewRecord={handleViewRecord}
            />
          </Form>
          <Button.Icon
            className="p-4"
            icon="chevronRight"
            title={commonText.next()}
            onClick={handleNext}
          />
        </div>
      ) : (
        <IIIFViewer
          baseUrl={getIIIFUrlFromVersion(
            activeIiifVersion,
            resource.get('attachmentLocation')
          )}
          title={attachmentsText.formatIiiF({
            version: activeIiifVersion.toString(),
            name: resource.get('origFilename'),
          })}
        />
      )}
    </Dialog>
  );
}
