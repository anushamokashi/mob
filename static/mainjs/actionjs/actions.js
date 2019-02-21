/*------------------------------------------------------------------------------
 *function for addaction in actions.html
 *----------------------------------------------------------------------------*/
$('.addactions').click(function(e) {
    debugger;
    var formdata = $("#addaction").serialize();
    var viewid = e.currentTarget.attributes['data-viewid'].value
    $.ajax({
        type: 'POST',
        url: "/transactionview/actions/" + viewid,
        data: formdata,
        //dataType: 'json',                 
        success: function(data) {

            ///alert("success");
            $('#viewtable').html("");
            $('#viewtable').html(data);
            var datatable = $('#tabcol').dataTable({
                "ordering": false,
            });
            $('#tabcol').DataTable();
            //$('#compModal').modal({'hide' : true});

            //$('#viewtable').datatable(
            //{ "ordering": false });

        },
        failure: function(data) {

            console.log(data)
        }
    });
});

/*------------------------------------------------------------------------------
 *Model function for add action in actions.html
 *----------------------------------------------------------------------------*/
function actionmodal(mevent){
    debugger;
    var txviewid = "";
    var actiontype = "";
    var viewcompedit = "";
    var actionModal = null;
    txviewid = mevent.currentTarget.attributes['data-transactionid'].value
    actiontype = mevent.currentTarget.attributes['data-actiontype'].value.toLowerCase()
    viewcompedit = '/actions/' + actiontype + 'action/' + actiontype + '/' + txviewid;
    $("#actionModal").on("show.bs.modal", function() {
        setTimeout(function() {
            if (actionModal == null) {
                actionModal = $.ajax(viewcompedit)
                    .done(function(data) {

                        $("#actionmodelbody").html(data);
                    })
                    .fail(function() {
                        alert("error");
                    });
            }
            return false;
        }, 500);

    });
    //$("#viewModal").modal('show'); 
    $('#actionModal').on('hidden.bs.modal', function(e) {
        console.log("Modal hidden");
        $('#actionmodelbody').modal('hide')
        $("#actionmodelbody").html("");
        $(this).data('modal', null);
        //$('#bodyCal').html("");
        //location.reload();
    });

};

/*------------------------------------------------------------------------------
 *function for save action
 *----------------------------------------------------------------------------*/
$(document).on('click', '#saveaction', function(e) {
    debugger;
    var exp = $('#expression').val();
    var formdata = $("#saveform").serialize();
    console.log(formdata);
    var viewid = e.currentTarget.attributes['data-transactionviewid'].value
    var actiontype = e.currentTarget.attributes['data-actiontype'].value
    $.ajax({
        type: 'POST',
        url: "/actions/saveaction/" + actiontype + "/" + viewid,
        data: formdata,
        contenttype: "application/x-www-form-urlencoded",
        success: function(data) {
            $('#actionModal').modal('hide');
            $("#divResults").empty();

            $("#divResults").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                $("#divResults").slideUp(500);
            });
            $("#createIoniclb").removeClass('bg-green-active');
            $("#createIoniclb").addClass('bg-blue');

        },
        error: function(data) {

            $("#divErrorMessages").empty();
            $("#divErrorMessages").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                $("#divErrorMessages").slideUp(500);
            });
        }
    });
});

/*------------------------------------------------------------------------------
 *function for new action
 *----------------------------------------------------------------------------*/
$(document).on('click', '#newaction', function(e) {
    debugger;
    var exp = $('#expression').val();
    var formdata = $("#newform").serialize();
    console.log(formdata);
    var viewid = e.currentTarget.attributes['data-transactionviewid'].value
    var actiontype = e.currentTarget.attributes['data-actiontype'].value
    $.ajax({
        type: 'POST',
        url: "/actions/newaction/" + actiontype + "/" + viewid,
        data: formdata,
        //dataType: 'json',                 
        success: function(data) {
            $('#actionModal').modal('hide');
            $("#divResults").empty();

            $("#divResults").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                $("#divResults").slideUp(500);
            });
            $("#createIoniclb").removeClass('bg-green-active');
            $("#createIoniclb").addClass('bg-blue');

        },
        error: function(data) {

            $("#divErrorMessages").empty();
            $("#divErrorMessages").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                $("#divErrorMessages").slideUp(500);
            });
        }
    });
});

/*------------------------------------------------------------------------------
 *function for delete action
 *----------------------------------------------------------------------------*/
$(document).on('click', '#deleteaction', function(e) {
    debugger;
    var exp = $('#expression').val();
    var formdata = $("#deleteform").serialize();
    console.log(formdata);
    var viewid = e.currentTarget.attributes['data-transactionviewid'].value
    var actiontype = e.currentTarget.attributes['data-actiontype'].value
    $.ajax({
        type: 'POST',
        url: "/actions/deleteaction/" + actiontype + "/" + viewid,
        data: formdata,
        //dataType: 'json',                 
        success: function(data) {
            $('#actionModal').modal('hide');
            $("#divResults").empty();

            $("#divResults").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                $("#divResults").slideUp(500);
            });
            $("#createIoniclb").removeClass('bg-green-active');
            $("#createIoniclb").addClass('bg-blue');

        },
        error: function(data) {

            $("#divErrorMessages").empty();
            $("#divErrorMessages").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                $("#divErrorMessages").slideUp(500);
            });
        }
    });
});

/*------------------------------------------------------------------------------
 *function for cancel action
 *----------------------------------------------------------------------------*/
$(document).on('click', '#cancelaction', function(e) {
    debugger;
    var exp = $('#expression').val();
    var formdata = $("#cancelform").serialize();
    console.log(formdata);
    var viewid = e.currentTarget.attributes['data-transactionviewid'].value
    var actiontype = e.currentTarget.attributes['data-actiontype'].value
    $.ajax({
        type: 'POST',
        url: "/actions/cancelaction/" + actiontype + "/" + viewid,
        data: formdata,
        //dataType: 'json',                 
        success: function(data) {
            $('#actionModal').modal('hide');
            $("#divResults").empty();

            $("#divResults").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                $("#divResults").slideUp(500);
            });
            $("#createIoniclb").removeClass('bg-green-active');
            $("#createIoniclb").addClass('bg-blue');


        },
        error: function(data) {
            $("#divErrorMessages").empty();
            $("#divErrorMessages").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                $("#divErrorMessages").slideUp(500);
            });
        }
    });
});

/*------------------------------------------------------------------------------
 *function for cancel action
 *----------------------------------------------------------------------------*/
$(document).on('click', '#searchaction', function(e) {
    debugger;
    var formdata = $("#searchform").serialize();
    console.log(formdata);
    var viewid = e.currentTarget.attributes['data-transactionviewid'].value
    var actiontype = e.currentTarget.attributes['data-actiontype'].value
    $.ajax({
        type: 'POST',
        url: "/actions/searchaction/" + actiontype + "/" + viewid,
        data: formdata,
        //dataType: 'json',                 
        success: function(data) {
            $('#actionModal').modal('hide');
            $("#divResults").empty();

            $("#divResults").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                $("#divResults").slideUp(500);
            });
            $("#createIoniclb").removeClass('bg-green-active');
            $("#createIoniclb").addClass('bg-blue');

        },
        error: function(data) {

            console.log(data)
        }
    });
});


// /*-----------------------------------------------------------------------------
// * Restriction For Expressiopn Input
// *----------------------------------------------------------------------------*/
// $(document).bind('cut copy paste','#expression',function(e){
   
//     e.preventDefault();

// });

// $(document).on('keypress', '#expression',function(e) {

// debugger;
// if (e.keyCode == 32 || e.keyCode > 64 && e.keyCode < 91)
//     return false;

// });



/*------------------------------------------------------------------------------
 *function for print format action
 *----------------------------------------------------------------------------*/
// $( '#txnprintformataction' ).submit( function( e ) {
// $(document).on('click', '#txnprintformataction', function(e) {

function txnprintformataction(e){
    debugger;
    // var formdata = new FormData($("#txnprintformatactionform")[0]);
    var formdata = $("#txnprintformatactionform").serialize();
    console.log(formdata);
    var viewid = e.currentTarget.attributes['data-transactionviewid'].value;
    var actiontype = e.currentTarget.attributes['data-actiontype'].value;
    console.log("/actions/printformataction/" + actiontype + "/" + viewid);
    $.ajax({
        type: 'POST',
        url: "/actions/printformataction/" + actiontype + "/" + viewid,
        data: formdata,
        //dataType: 'json', 
        // processData: false,
        // contentType: false,             
        success: function(data) {
            debugger;
            console.log(data);

            if (data=="success"){

                $('#actionModal').modal('hide');
                $("#divResults").empty();

                $("#divResults").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                    $("#divResults").slideUp(500);
                });
                $("#createIoniclb").removeClass('bg-green-active');
                $("#createIoniclb").addClass('bg-blue');

            }
            if (data=="failure"){
                e.preventDefault();
                $('#actionModal').modal('hide');
                $("#divErrorMessages").empty();

                $("#divErrorMessages").fadeTo(2000, 500).append("<h4>Alert!</h4>Save Failed.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorMessages").slideUp(500);
                });
                $("#createIoniclb").removeClass('bg-green-active');
                $("#createIoniclb").addClass('bg-blue');

            }
            

        },
        error: function(data) {

            debugger;

            console.log(data);

            $('#actionModal').modal('hide');
                $("#divErrorMessages").empty();

                $("#divErrorMessages").fadeTo(2000, 500).append("<h4>Alert!</h4>Save Failed.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorMessages").slideUp(500);
                });
                $("#createIoniclb").removeClass('bg-green-active');
                $("#createIoniclb").addClass('bg-blue');
            e.preventDefault();
        }
    });
    // e.preventDefault();
};

/*------------------------------------------------------------------------------
  Function for Forcing upper case letter in paramater field
*----------------------------------------------------------------------------*/
// $(document).on('keypress', '#id_parameter',function(e) {

//     debugger;
//     if (e.keyCode > 97 && e.keyCode < 123)
//         return false;
    
// });


/*------------------------------------------------------------------------------
 *function for googlesync action
 *----------------------------------------------------------------------------*/
// $(document).on('click', '#newaction', function(e) {
function googlesyncaction(e){
    debugger;
    var exp = $('#expression').val();
    var formdata = $("#googlesyncform").serialize();
    console.log(formdata);
    var viewid = e.currentTarget.attributes['data-transactionviewid'].value
    var actiontype = e.currentTarget.attributes['data-actiontype'].value
    $.ajax({
        type: 'POST',
        url: "/actions/googlesyncaction/" + actiontype + "/" + viewid,
        data: formdata,
        //dataType: 'json',                 
        success: function(data) {
            $('#actionModal').modal('hide');
            $("#divResults").empty();

            $("#divResults").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                $("#divResults").slideUp(500);
            });
            $("#createIoniclb").removeClass('bg-green-active');
            $("#createIoniclb").addClass('bg-blue');

        },
        error: function(data) {

            $("#divErrorMessages").empty();
            $("#divErrorMessages").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                $("#divErrorMessages").slideUp(500);
            });
        }
    });
}

