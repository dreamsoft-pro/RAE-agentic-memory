export function Dialogs(){
    function modal(){}
    function toast(content){
        /*const toast = new bootstrap.Toast(toastLiveExample)

        toast.show()*/

    }

    function info(text) {
        const html = `<div class="toast" role="alert" aria-live="assertive" aria-atomic="true" id="infoToast">
  <div class="toast-header">
    <strong class="me-auto">Info</strong>
    <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
  </div>
  <div class="toast-body">
    ${text}
  </div>
</div>`
        $('#toastContainer').append(html)
        const toast = new bootstrap.Toast('#infoToast', {})
        $('#infoToast').on('hidden.bs.toast', function(){
            $(this).remove()
        })
        toast.show()
    }
    function error(err){
        info(`error ${text} TODO`)
    }
    function warning(text){
        info(`wanring ${text} TODO`)
    }
    let modalInstance;
    const modalInstances={};

    function modalCreate(element,config){
        modalInstance=new bootstrap.Modal(element,config)
        modalInstances[element]=modalInstance
        return modalInstance
    }
    function modalHide(element){
        if(element && modalInstances[element]){
            modalInstances[element].hide()
        }else if(modalInstance){
            modalInstance.hide()
        }

    }
    return{
        modalCreate,
        modalHide,
        info,
        error,
        warning
    }
}
