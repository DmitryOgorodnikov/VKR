(function () {
    if (typeof window.CustomEvent === "function") return false;
    function CustomEvent(event, params) {
        params = params || { bubbles: false, cancelable: false, detail: null };
        var evt = document.createEvent('CustomEvent');
        evt.initCustomEvent(event, params.bubbles, params.cancelable, params.detail);
        return evt;
    }
    window.CustomEvent = CustomEvent;
})();

$modal = function (options) {
    var
        _elemModal,
        _eventShowModal,
        _eventHideModal,
        _hiding = false,
        _destroyed = false,
        _animationSpeed = 200;

    function _createModal(options) {
        var
            elemModal = document.createElement('div'),
            modalTemplate = '<div class="modal__backdrop backdrop" data-dismiss="modal"><div class="modal__content content"><div class="modal__header header"><div class="modal__title title" data-modal="title">{{title}}</div></div><div class="modal__body body" data-modal="content">{{content}}</div>{{footer}}</div></div>',
            modalFooterTemplate = '<div class="modal__footer footer">{{buttons}}</div>',
            modalButtonTemplate = '<button type="button" class="{{button_class}}" data-handler={{button_handler}}>{{button_text}}</button>',
            modalHTML,
            modalFooterHTML = '';

        elemModal.classList.add('modal');
        modalHTML = modalTemplate.replace('{{title}}', options.title || 'Новое окно');
        modalHTML = modalHTML.replace('{{content}}', options.content || '');
        if (options.footerButtons) {
            for (var i = 0, length = options.footerButtons.length; i < length; i++) {
                var modalFooterButton = modalButtonTemplate.replace('{{button_class}}', options.footerButtons[i].class);
                modalFooterButton = modalFooterButton.replace('{{button_handler}}', options.footerButtons[i].handler);
                modalFooterButton = modalFooterButton.replace('{{button_text}}', options.footerButtons[i].text);
                modalFooterHTML += modalFooterButton;
            }
            modalFooterHTML = modalFooterTemplate.replace('{{buttons}}', modalFooterHTML);
        }
        modalHTML = modalHTML.replace('{{footer}}', modalFooterHTML);
        elemModal.innerHTML = modalHTML;
        document.body.appendChild(elemModal);
        return elemModal;
    }

    function _showModal() {
        if (!_destroyed && !_hiding) {
            _elemModal.classList.add('show');
            document.dispatchEvent(_eventShowModal);
        }
    }

    function _hideModal() {
        _hiding = true;
        _elemModal.classList.remove('show');
        _elemModal.classList.add('hiding');
        setTimeout(function () {
            _elemModal.classList.remove('hiding');
            _hiding = false;
        }, _animationSpeed);
        document.dispatchEvent(_eventHideModal);
        location.reload();
    }

    function _handlerCloseModal(e) {
        if (e.target.dataset.dismiss === 'modal') {
            _hideModal();
        }
    }

    function _handlerOkModal(e) {
        if (e.target.dataset.handler === 'handlerOkModal') {
            callPrint();
            _hideModal();
        }
    }

    _elemModal = _createModal(options || {});


    _elemModal.addEventListener('click', _handlerCloseModal);
    _elemModal.addEventListener('click', _handlerOkModal);
    _eventShowModal = new CustomEvent('show.modal', { detail: _elemModal });
    _eventHideModal = new CustomEvent('hide.modal', { detail: _elemModal });

    return {
        show: _showModal,
        hide: _hideModal,
        destroy: function () {
            _elemModal.parentElement.removeChild(_elemModal),
                _elemModal.removeEventListener('click', _handlerCloseModal),
                _elemModal.removeEventListener('click', _handlerOkModal),
                _destroyed = true;
        },
        setContent: function (html) {
            _elemModal.querySelector('[data-modal="content"]').innerHTML = html;
        },
        setTitle: function (text) {
            _elemModal.querySelector('[data-modal="title"]').innerHTML = text;
        }
    }
};

function callPrint() {
    var printTitle = document.getElementById('print-title').innerHTML;
    var printText = document.getElementById('print-text').innerHTML;
    var windowPrint = window.open('', '', 'left=50,top=50,width=800,height=640,toolbar=0,scrollbars=1,status=0');
    windowPrint.document.write('<p><center style="font-size: 250px;">' + printTitle + '</center></p>');
    windowPrint.document.write('<p><center style="font-size: 250px;">' + printText + '</center></p>');

    var date = new Date()

    var hours = date.getHours()
    if (hours < 10) hours = '0' + hours

    var minutes = date.getMinutes()
    if (minutes < 10) minutes = '0' + minutes

    var seconds = date.getSeconds()
    if (seconds < 10) seconds = '0' + seconds

    var days = date.getDate()
    if (days < 10) days = '0' + days

    var months = date.getMonth() + 1
    if (months < 10) months = '0' + months

    var years = date.getFullYear()

    document.getElementById('year').innerHTML = years
    windowPrint.document.write('<p><center style="font-size: 100px;">' + hours + ':' + minutes + ':' + seconds + ' ' + days + '.' + months + '.' + years + '</center></p>');
    windowPrint.document.write('<p><center style="font-size: 50px;">' + $('#opsname').attr("name") + '</center></p>');
    windowPrint.document.close();
    windowPrint.focus();
    windowPrint.print();
    windowPrint.close();
}