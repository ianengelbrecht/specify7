"use strict";

import $ from 'jquery';
import 'jquery-contextmenu';
import 'jquery-ui';
import {ErrorView} from './errorview';
import NotFoundView from './notfoundview';
import router from './router';
import systemInfo from './systeminfo';
import commonText from './localization/common';
import {setTitle} from "./components/hooks";

global.jQuery = $;

var currentView;
    var versionMismatchWarned = false;


    // setup basic routes.
    router
        .route('*whatever', 'notFound', function() {
            setCurrentView(new NotFoundView());
        })
        .route('test_error/', 'testError', function() {
            $.get('/api/test_error/');
        });

    $.ui.dialog.prototype._focusTabbable = function(){
        let previousFocusedElement = document.activeElement;
        this.uiDialog.focus();
        // Return focus to the previous focused element on dialog close
        this.uiDialog.on('dialogbeforeclose',()=>
            previousFocusedElement?.focus()
        );

        /*
         * Make title non-bold by adding 'ui-dialog-with-header' className to
         * non-React dialogs that have headers (React dialogs do the same in
         * modaldialog.tsx)
         * */
        if(!this.options.dialogClass.split(' ').includes('ui-dialog-react'))
            this.uiDialog.on(
                'dialogopen',
                () =>
                    this.uiDialog[0].getElementsByTagName('h2').length &&
                    this.uiDialog[0].classList.add('ui-dialog-with-header')
            );

        // Set proper aria attributes
        this.uiDialog[0].setAttribute('role','dialog');
        if(this.options.modal)
            this.uiDialog[0].setAttribute('aria-modal','true');
        this.uiDialog.find('.ui-dialog-titlebar')[0]?.setAttribute('role','header');
        this.uiDialog.find('.ui-dialog-buttonpane')[0]?.setAttribute('role','menu');
    };

    /**
     * Gets rid of any backbone view currently showing
     * and replaces it with the rendered view given
     * also manages other niceties involved in changing views
     */
    let isFirstRender = true;
    export function setCurrentView(view) {
        // Remove old view
        currentView && currentView.remove();
        const main = $('main');
        main.empty();

        /*
         * Close any open dialogs, unless rendering for the first time
         * (e.g, UserTools dialog can be opened by the user before first render)
         * */
        if(!isFirstRender)
            $('.ui-dialog:not(.ui-dialog-no-close)')
                .find('.ui-dialog-content:not(.ui-dialog-persistent)')
                .dialog('close');
        isFirstRender = false;

        currentView = view;
        currentView.render();
        main.append(currentView.el);
        main[0].focus();

        if (typeof currentView.title === 'string')
            setTitle(currentView.title);
        else if (typeof currentView.title === 'function')
            setTitle(currentView.title(currentView));

        Array.from(
          document.getElementById('site-nav').getElementsByTagName('a'),
          (link)=>{
              const path = link.getAttribute('data-path');
              if(window.location.pathname.startsWith(path))
                  link.setAttribute('aria-current','page');
              else
                  link.removeAttribute('aria-current');
          }
       );

        if (systemInfo.specify6_version !== systemInfo.database_version && !versionMismatchWarned) {
            $(`<div role="alert">
                ${commonText('versionMismatchDialogHeader')}
                <p>
                    ${commonText('versionMismatchDialogMessage')(
                        systemInfo.specify6_version,
                        systemInfo.database_version
                    )}
                </p>
                <p>${commonText('versionMismatchSecondDialogMessage')}</p>
            </div>`).dialog({
                title: commonText('versionMismatchDialogTitle'),
                modal: true,
            });
            versionMismatchWarned = true;
        }
    }

    export function handleError(jqxhr) {
        setCurrentView(new ErrorView({
            header: jqxhr.status,
            message: jqxhr.statusText
        }));
        jqxhr.errorHandled = true;
    }