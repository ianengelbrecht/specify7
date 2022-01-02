'use strict';

import $ from 'jquery';
import React from "react";

import * as businessRules from './businessrules';
import {UnhandledErrorView} from './errorview';
import commonText from './localization/common';
import csrftoken from "./csrftoken";
import {csrfSafeMethod} from "./ajax";
import {handlePromiseReject} from "./components/wbplanview";
import * as navigation from './navigation';

$.ajaxSetup({
  beforeSend: function (xhr, settings) {
    if (!csrfSafeMethod.has(settings.type.toUpperCase()) && !this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});
$(document).ajaxError(handleUnexpectedError);

function handleUnexpectedError(event, jqxhr, settings, exception) {
  if (jqxhr.errorHandled) return; // Not unexpected.
  if (jqxhr.status === 403) {
    $(`<div role="alert">
        ${commonText('sessionTimeOutDialogHeader')}
        <p>${commonText('sessionTimeOutDialogMessage')}</p>
    </div>`)
      .appendTo('body')
      .dialog({
        title: commonText('sessionTimeOutDialogTitle'),
        modal: true,
        dialogClass: 'ui-dialog-no-close',
        buttons: [
          {
            text: commonText('logIn'),
            click: function () {
              window.location = '/accounts/login/?next=' + window.location.href;
            },
          },
        ],
      });
    return;
  }
  new UnhandledErrorView({response: jqxhr.responseText}).render();

  console.log({event, jqxhr, settings, exception});
}


const tasksPromise = Promise.all([
  import('./welcometask'),
  import('./datatask'),
  import('./querytask'),
  import('./treetask'),
  import('./expresssearchtask'),
  import('./datamodeltask'),
  import('./attachmentstask'),
  import('./wbtask'),
  import('./wbimporttask'),
  import('./wbplantask'),
  import('./appresourcetask'),
  import('./components/lifemapperwrapper'),
]).then((tasks) => tasks.forEach(({ default: task }) => task()));


export default function appStart() {
  console.info('specify app starting');
  businessRules.enable(true);
  navigation.start();
  tasksPromise.catch(handlePromiseReject);
};
