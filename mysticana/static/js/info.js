// NOTICE!!! Initially embedded in our docs this JavaScript
// file contains elements that can help you create reproducible
// use cases in StackBlitz for instance.
// In a real project please adapt this content to your needs.
// ++++++++++++++++++++++++++++++++++++++++++

/*!
 * JavaScript for Bootstrap's docs (https://getbootstrap.com/)
 * Copyright 2011-2022 The Bootstrap Authors
 * Copyright 2011-2022 Twitter, Inc.
 * Licensed under the Creative Commons Attribution 3.0 Unported License.
 * For details, see https://creativecommons.org/licenses/by/3.0/.
 */

/* global bootstrap: false */

(() => {
  'use strict'

  // --------
  // Tooltips
  // --------
  // Instantiate all tooltips in a docs or StackBlitz page
  document.querySelectorAll('[data-bs-toggle="tooltip"]')
    .forEach(tooltip => {
      new bootstrap.Tooltip(tooltip)
    })

  // --------
  // Popovers
  // --------
  // Instantiate all popovers in a docs or StackBlitz page
  document.querySelectorAll('[data-bs-toggle="popover"]')
    .forEach(popover => {
      new bootstrap.Popover(popover)
    })

  // -------------------------------
  // Toasts
  // -------------------------------
  // Used by 'Placement' example in docs or StackBlitz
  const toastPlacement = document.getElementById('toastPlacement')
  if (toastPlacement) {
    document.getElementById('selectToastPlacement').addEventListener('change', function () {
      if (!toastPlacement.dataset.originalClass) {
        toastPlacement.dataset.originalClass = toastPlacement.className
      }

      toastPlacement.className = `${toastPlacement.dataset.originalClass} ${this.value}`
    })
  }

  // Instantiate all toasts in a docs page only
  document.querySelectorAll('.bd-example .toast')
    .forEach(toastNode => {
      const toast = new bootstrap.Toast(toastNode, {
        autohide: false
      })

      toast.show()
    })

  // Instantiate all toasts in a docs page only
  const toastTrigger = document.getElementById('liveToastBtn')
  const toastLiveExample = document.getElementById('liveToast')
  if (toastTrigger) {
    toastTrigger.addEventListener('click', () => {
      const toast = new bootstrap.Toast(toastLiveExample)

      toast.show()
    })
  }

  // -------------------------------
  // Alerts
  // -------------------------------
  // Used in 'Show live toast' example in docs or StackBlitz
  const alertPlaceholder = document.getElementById('liveAlertPlaceholder')
  const alertTrigger = document.getElementById('liveAlertBtn')

  const appendAlert = (message, type) => {
    const wrapper = document.createElement('div')
    wrapper.innerHTML = [
      `<div class="alert alert-${type} alert-dismissible" role="alert">`,
      `   <div>${message}</div>`,
      '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
      '</div>'
    ].join('')

    alertPlaceholder.append(wrapper)
  }

  if (alertTrigger) {
    alertTrigger.addEventListener('click', () => {
      appendAlert('Nice, you triggered this alert message!', 'success')
    })
  }

  // -------------------------------
  // Checks & Radios
  // -------------------------------
  // Indeterminate checkbox example in docs and StackBlitz
  document.querySelectorAll('.bd-example-indeterminate [type="checkbox"]')
    .forEach(checkbox => {
      if (checkbox.id.includes('Indeterminate')) {
        checkbox.indeterminate = true
      }
    })

  // -------------------------------
  // Links
  // -------------------------------
  // Disable empty links in docs examples only
  document.querySelectorAll('.bd-content [href="#"]')
    .forEach(link => {
      link.addEventListener('click', event => {
        event.preventDefault()
      })
    })

  // -------------------------------
  // Modal
  // -------------------------------
  // Modal 'Varying modal content' example in docs and StackBlitz
  const exampleModal = document.getElementById('exampleModal')
  if (exampleModal) {
    exampleModal.addEventListener('show.bs.modal', event => {
      // Button that triggered the modal
      const button = event.relatedTarget
      // Extract info from data-bs-* attributes
      const recipient = button.getAttribute('data-bs-whatever')

      // Update the modal's content.
      const modalTitle = exampleModal.querySelector('.modal-title')
      const modalBodyInput = exampleModal.querySelector('.modal-body input')

      modalTitle.textContent = `New message to ${recipient}`
      modalBodyInput.value = recipient
    })
  }

  // -------------------------------
  // Offcanvas
  // -------------------------------
  // 'Offcanvas components' example in docs only
  const myOffcanvas = document.querySelectorAll('.bd-example-offcanvas .offcanvas')
  if (myOffcanvas) {
    myOffcanvas.forEach(offcanvas => {
      offcanvas.addEventListener('show.bs.offcanvas', event => {
        event.preventDefault()
      }, false)
    })
  }

  window.addEventListener("resize", AutoScaleTable); //Масштабируем страницу при растягивании окна

window.addEventListener("load",AutoScaleTable); //Масштабируем таблицу после загрузки

function AutoScaleTable()
{
    let width = window.innerWidth; //Ширина окна
    //Если вы хотите проверять по размеру экрана, то вам нужно свойство window.screen.width
    let val_elems = document.getElementsByClassName('table-elems').length

    if(width > 720)
    {
        //console.log({width});
        for(let i=0; i<val_elems; i++){
            document.getElementsByClassName('table-elems')[i].classList.add('t-show');
        }
        for(let i=0; i<document.getElementsByClassName('table-rows').length; i++){
            document.getElementsByClassName('table-rows')[i].classList.remove('t-show');
        }

        // document.getElementsByClassName('table-rows')[0].style= "display: none";
   	 //  console.log({width});
    }
    else if(width < 720)
    {
         for( let i=0; i<val_elems; i++){
             console.log(i);
            document.getElementsByClassName('table-elems')[i].classList.remove('t-show');
        }
         for(let i=0; i<document.getElementsByClassName('table-rows').length; i++){
            document.getElementsByClassName('table-rows')[i].classList.add('t-show');
        }

        // document.getElementsByClassName('table-rows')[0].style= "display: revert ;";
   	 // console.log({width});
    }
}
//   if (document.table-main-calc.clientWidth < 1200) {
//  console.log("ugyuui")
// } else {
// console.log("123456")
// };
})()


function blockForm(f) {
    // Проверка на заполненность даты
    let textarea = f.datein.value;
    console.log(textarea.length);
    if (textarea.length != 0){f.submit.disabled=0;}
    else{f.submit.disabled=1;}
}

function blockForm2(f) {
    // Проверка на заполненность даты
    let textarea2 = f.txt.value;
    console.log(textarea2.length);
    if (textarea2.length != 0){f.submit.disabled=0;}
    else{f.submit.disabled=1;}
}

   //
   //  if (f.datein.value == null) f.submit.disabled = 0
   // //if (f.matrix2.checked) f.submit.disabled = 0
   //  // В противном случае вновь блокируем кнопку
   //  else f.submit.disabled = 1}