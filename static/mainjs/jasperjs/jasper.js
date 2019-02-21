/*------------------------------------------------------------------------------
  Function for Add Jasper modal in jasperindex.html
*----------------------------------------------------------------------------*/
function addjasperModal(e) {
    debugger;
    var url = '/jasper/jasperadd/';
    var model = null;
    $("#jasperaddmodal").on("shown.bs.modal",function() { 
        setTimeout(function() {
            if (model == null) {    
            model = $.ajax(url)
                .done(function(data) {
                    $("#jasperaddmodalBody").html(data);
                })
                .fail(function() {
                    alert("error");
                });
            }
        },500);                
    }); 

    $('#jasperaddmodal').on('hidden.bs.modal', function(e) {
        console.log("Modal hidden");
        $('#jasperaddmodalBody').modal('hide');
        $(this).data('modal', null);
        $("#jasperaddmodalBody").html("");
    });
};
/*------------------------------------------------------------------------------
  Function for on change of viewtype
*----------------------------------------------------------------------------*/
$("#id_Views").change(function() {
    debugger;
    var viewValue = $(this).val();

    if (viewValue == "Transaction"){
        $("#rptviewDiv")[0].style.display = "none";
        $("#txviewDiv")[0].style.display = "block";

    }
    else if (viewValue == "Report"){
        $("#txviewDiv")[0].style.display = "none";
        $("#rptviewDiv")[0].style.display = "block";
    }
});

/*------------------------------------------------------------------------------
  Function for Forcing upper case letter in paramater field
*----------------------------------------------------------------------------*/
// $(document).on('keypress', '#id_parameter',function(e) {

//     debugger;
//     if (e.keyCode > 97 && e.keyCode < 123)
//         return false;
    
// });


/*-----------------------------------------------------------------------------
  Function for Add Role in roleindex.html
*----------------------------------------------------------------------------*/
// function saveJsper(e) {
//     debugger;
   
  
//     var formdata = $("#jasperform").serialize();

//     $.ajax({
//         type: 'POST',
//         url: "/jasper/jasperadd/",
//         data: formdata,          
//         success: function(data) {
//             debugger;
//             if (data == "Failure"){
//                 console.log(data)
//                 $("#divErrorJasper").empty();
//                 $("#divErrorJasper").fadeTo(2000, 500).append("<h4>Alert!</h4>Save Failed. Role already exist.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
//                     $("#divErrorJasper").slideUp(500);
//                 });

//             }
 
//             else if(data == "Success"){
//                 debugger;
//                 $("#divResultJasper").empty();

//                 $("#divResultJasper").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
//                     $("#divResultJasper").slideUp(500);
//                 });
//                 window.location.reload();
//             }
            
//         },
//         failure: function(data) {
//             debugger;
//             console.log(data)
//             $(saveclose).click();
//             $("#divErrorJasper").empty();
//             $("#divErrorJasper").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
//                 $("#divErrorJasper").slideUp(500);
//             });
//         }
//     });
//     e.preventDefault(); 
    
// };


$( '#jasperform' ).submit( function( e ) {
    debugger;
    console.log(this.getData());
    
    $.ajax( {
        url:  "/jasper/jasperadd/",
        type: 'POST',
        data: new FormData(this),
        processData: false,
        contentType: false,
        success: function(data) {
            debugger;
            if (data == "Failure"){
                console.log(data)
                $("#divErrorJasper").empty();
                $("#divErrorJasper").fadeTo(2000, 500).append("<h4>Alert!</h4>Save Failed. Role already exist.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorJasper").slideUp(500);
                });

            }

            else if(data == "Success"){
                debugger;
                $("#divResultJasper").empty();

                $("#divResultJasper").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                    $("#divResultJasper").slideUp(500);
                });
                window.location.reload();
            }
            
        },
        failure: function(data) {
            debugger;
            console.log(data)
            $(saveclose).click();
            $("#divErrorJasper").empty();
            $("#divErrorJasper").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                $("#divErrorJasper").slideUp(500);
            });
        }
    });
    e.preventDefault(); 
});


