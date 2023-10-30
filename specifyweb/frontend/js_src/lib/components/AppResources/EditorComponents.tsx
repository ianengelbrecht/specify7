import { json } from '@codemirror/lang-json';
import { xml } from '@codemirror/lang-xml';
import { indentUnit, StreamLanguage } from '@codemirror/language';
import { properties } from '@codemirror/legacy-modes/mode/properties';
import type { Diagnostic } from '@codemirror/lint';
import { lintGutter } from '@codemirror/lint';
import type { Extension } from '@codemirror/state';
import { EditorState } from '@codemirror/state';
import { EditorView } from 'codemirror';
import React from 'react';
import type { LocalizedString } from 'typesafe-i18n';

import { useBooleanState } from '../../hooks/useBooleanState';
import { commonText } from '../../localization/common';
import { notificationsText } from '../../localization/notifications';
import { resourcesText } from '../../localization/resources';
import type { RA } from '../../utils/types';
import { filterArray } from '../../utils/types';
import { Button } from '../Atoms/Button';
import { DataEntry } from '../Atoms/DataEntry';
import { LoadingContext } from '../Core/Contexts';
import { getField } from '../DataModel/helpers';
import type { SerializedResource } from '../DataModel/helperTypes';
import type { SpecifyResource } from '../DataModel/legacyTypes';
import { useSaveBlockers } from '../DataModel/saveBlockers';
import type { SpAppResource, SpViewSetObj } from '../DataModel/types';
import { Dialog } from '../Molecules/Dialog';
import { downloadFile, FilePicker, fileToText } from '../Molecules/FilePicker';
import { userPreferences } from '../Preferences/userPreferences';
import type { BaseSpec } from '../Syncer';
import type { SimpleXmlNode } from '../Syncer/xmlToJson';
import { jsonLinter, xmlLinter } from './codeMirrorLinters';
import type { getResourceType } from './filtersHelpers';
import { getAppResourceExtension } from './hooks';
import { appResourceSubTypes, appResourceTypes } from './types';

export const appResourceIcon = (
  type: ReturnType<typeof getResourceType>
): JSX.Element => (
  <span
    /*
     * FEATURE: include this title in aria-describedby on the button itself
     *   so that screen readers announce the type after the name
     */
    aria-hidden
    title={
      type === 'viewSet'
        ? resourcesText.formDefinitions()
        : appResourceSubTypes[type].label
    }
  >
    {type === 'viewSet'
      ? appResourceTypes.viewSets.icon
      : appResourceSubTypes[type].icon}
  </span>
);

export function AppResourceEditButton({
  title,
  children,
}: {
  readonly title: LocalizedString;
  readonly children: JSX.Element;
}): JSX.Element {
  const [isEditingMeta, handleEditingMeta, handleEditedMeta] =
    useBooleanState();
  return (
    <>
      <DataEntry.Edit onClick={handleEditingMeta} />
      {isEditingMeta && (
        <Dialog
          buttons={commonText.close()}
          dimensionsKey="AppResourceEdit"
          header={title}
          onClose={handleEditedMeta}
        >
          {children}
        </Dialog>
      )}
    </>
  );
}

export function AppResourceLoad({
  onLoaded: handleLoaded,
}: {
  readonly onLoaded: (data: string, mimeType: string) => void;
}): JSX.Element {
  const [isOpen, handleOpen, handleClose] = useBooleanState();
  const loading = React.useContext(LoadingContext);
  return (
    <>
      <Button.Success className="whitespace-nowrap" onClick={handleOpen}>
        {resourcesText.loadFile()}
      </Button.Success>
      {isOpen && (
        <Dialog
          buttons={commonText.cancel()}
          header={resourcesText.loadFile()}
          onClose={handleClose}
        >
          <FilePicker
            acceptedFormats={undefined}
            onSelected={(file): void =>
              loading(
                fileToText(file)
                  .then((data) => handleLoaded(data, file.type))
                  .finally(handleClose)
              )
            }
          />
        </Dialog>
      )}
    </>
  );
}

export function AppResourceDownload({
  resource,
  data,
}: {
  readonly resource: SerializedResource<SpAppResource | SpViewSetObj>;
  readonly data: string;
}): JSX.Element {
  const loading = React.useContext(LoadingContext);
  return (
    <Button.Success
      className="whitespace-nowrap"
      disabled={data.length === 0}
      onClick={(): void =>
        loading(
          downloadFile(
            `${resource.name}.${getAppResourceExtension(resource)}`,
            data
          )
        )
      }
    >
      {notificationsText.download()}
    </Button.Success>
  );
}

export function useIndent(): string {
  const [indentSize] = userPreferences.use(
    'appResources',
    'behavior',
    'indentSize'
  );
  const [indentWithTab] = userPreferences.use(
    'appResources',
    'behavior',
    'indentWithTab'
  );
  return indentWithTab ? '\t' : ' '.repeat(indentSize);
}

/**
 * Use useIndent() instead whenever possible
 */
export function getIndent(): string {
  const indentSize = userPreferences.get(
    'appResources',
    'behavior',
    'indentSize'
  );
  const indentWithTab = userPreferences.get(
    'appResources',
    'behavior',
    'indentWithTab'
  );
  return indentWithTab ? '\t' : ' '.repeat(indentSize);
}

export function useCodeMirrorExtensions(
  resource: SerializedResource<SpAppResource | SpViewSetObj>,
  appResource: SpecifyResource<SpAppResource | SpViewSetObj>,
  xmlSpec: (() => BaseSpec<SimpleXmlNode>) | undefined
): RA<Extension> {
  const [lineWrap] = userPreferences.use(
    'appResources',
    'behavior',
    'lineWrap'
  );
  const [indentSize] = userPreferences.use(
    'appResources',
    'behavior',
    'indentSize'
  );
  const indentCharacter = useIndent();

  const mode = React.useMemo(
    () => getAppResourceExtension(resource),
    [resource]
  );
  const [extensions, setExtensions] = React.useState<RA<Extension>>([]);
  const [_blockers, setBlockers] = useSaveBlockers(
    appResource,
    React.useMemo(
      () => getField(appResource.specifyTable, 'spAppResourceDatas'),
      [appResource.specifyTable]
    )
  );

  React.useEffect(() => {
    const handleLinted = (results: RA<Diagnostic>): void =>
      setBlockers(
        filterArray(
          results.map(({ message, severity }) =>
            severity === 'error' ? message : undefined
          )
        )
      );

    const language =
      mode === 'json'
        ? [json(), jsonLinter(handleLinted)]
        : mode === 'properties'
        ? [StreamLanguage.define(properties)]
        : mode === 'jrxml' || mode === 'xml'
        ? [xml(), xmlLinter(xmlSpec?.())(handleLinted)]
        : [];
    setExtensions([
      ...language,
      ...(lineWrap ? [EditorView.lineWrapping] : []),
      indentUnit.of(indentCharacter),
      EditorState.tabSize.of(indentSize),
      lintGutter(),
    ]);

    return (): void => setBlockers([]);
  }, [
    appResource,
    mode,
    lineWrap,
    indentCharacter,
    indentSize,
    xmlSpec,
    setBlockers,
  ]);

  return extensions;
}
