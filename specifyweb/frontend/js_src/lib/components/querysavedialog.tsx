import React from 'react';

import type { SpQuery } from '../datamodel';
import type { SpecifyResource } from '../legacytypes';
import commonText from '../localization/common';
import queryText from '../localization/query';
import { Button, Form, Input, Label, Submit } from './basic';
import { useId } from './hooks';
import { Dialog, LoadingScreen } from './modaldialog';
import { crash } from './errorboundary';
import { userInformation } from '../userinfo';

async function doSave(
  query: SpecifyResource<SpQuery>,
  name: string,
  isSaveAs: boolean
): Promise<number> {
  const clonedQuery = isSaveAs ? query.clone() : query;
  clonedQuery.set('name', name.trim());

  if (isSaveAs) clonedQuery.set('specifyUser', userInformation.resource_uri);
  return new Promise((resolve) => {
    clonedQuery.save().then(() => resolve(clonedQuery.id));
  });
}

export function QuerySaveDialog({
  isSaveAs,
  query,
  onClose: handleClose,
  onSaved: handleSaved,
}: {
  readonly isSaveAs: boolean;
  readonly query: SpecifyResource<SpQuery>;
  readonly onClose: () => void;
  readonly onSaved: (queryId: number) => void;
}): JSX.Element {
  const id = useId('id');
  const [name, setName] = React.useState<string>(query.get('name'));
  const [isLoading, setIsLoading] = React.useState(false);

  React.useEffect(() => {
    if (query.isNew() || isSaveAs) return;
    setIsLoading(true);
    doSave(query, name, isSaveAs).then(handleClose).catch(crash);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return isLoading ? (
    <LoadingScreen />
  ) : (
    <Dialog
      title={queryText('saveQueryDialogTitle')}
      header={
        isSaveAs
          ? queryText('saveClonedQueryDialogHeader')
          : queryText('saveQueryDialogHeader')
      }
      onClose={handleClose}
      buttons={
        <>
          <Button.DialogClose>{commonText('close')}</Button.DialogClose>
          <Submit.Blue form={id('form')}>{commonText('save')}</Submit.Blue>
        </>
      }
    >
      <p>
        {isSaveAs
          ? queryText('saveClonedQueryDialogMessage')
          : queryText('saveQueryDialogMessage')}
      </p>
      <Form
        className="contents"
        id={id('form')}
        onSubmit={(event): void => {
          event.preventDefault();
          setIsLoading(true);
          doSave(query, name, isSaveAs).then(handleSaved).catch(crash);
        }}
      >
        <Label>
          {queryText('queryName')}
          <Input
            type="text"
            autoComplete="on"
            spellCheck="true"
            required
            value={name}
            onChange={({ target }): void => setName(target.value)}
          />
        </Label>
      </Form>
    </Dialog>
  );
}
