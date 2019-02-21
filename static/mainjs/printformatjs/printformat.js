function addPFModal(event){
    debugger;
    var dpconf = "";
    var modal = null;
    actionconf = "/printformat/addPFModal/";
    $("#pfAddModal").on("show.bs.modal", function() {
        if (modal == null) {
            var modal = $.ajax(actionconf)
            
            .done(function(data) {
                $("#pfAddModalBody").html(data);
            })
            
            .fail(function() {
                alert("error");
            });
        }

    });
    $('#pfAddModal').on('hidden.bs.modal', function () {
        $("#pfAddModalBody").modal('hide');
        $(this).data('modal', null);
        $("#pfAddModalBody").html("");
    })
};

function printformatsave(event){
    debugger;
    var formdata = new FormData($("#printformatform")[0]);
   
    // for (var [key, value] of formdata.entries()) { 
    //     console.log(key, value);
    // }
    $.ajax({
        type:'POST',
        url:"/printformat/savePF/",
        data:formdata,
        processData: false,
        contentType: false, 
        success:function(res){
            debugger
            console.log(res);

            if (res == "TITLE"){
                console.log(res)
                $("#divErrorPFAdd").empty();
                $("#divErrorPFAdd").fadeTo(2000, 500).append("<h4>Alert!</h4>Title already exist.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorPFAdd").slideUp(500);
                });

            }
            else if (res == "Failure"){
                console.log(res)
                $("#divErrorPFAdd").empty();
                $("#divErrorPFAdd").fadeTo(2000, 500).append("<h4>Alert!</h4>Save Failed").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorPFAdd").slideUp(500);
                });

            }

            else if (res == "DO"){
                console.log(res)
                $("#divErrorPFAdd").empty();
                $("#divErrorPFAdd").fadeTo(2000, 500).append("<h4>Alert!</h4>Display Order should be unique.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorPFAdd").slideUp(500);
                });

            }
    
            else if(res == "Success"){
                debugger;
                $("#divResultPFAdd").empty();

                $("#divResultPFAdd").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                    $("#divResultPFAdd").slideUp(500);
                });
                window.location.reload();
            }
           
        },
        error: function(data) {
            debugger
            console.log(data);
            $("#divErrorPFAdd").empty();
                $("#divErrorPFAdd").fadeTo(2000, 500).append("<h4>Alert!</h4>Save Failed").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorPFAdd").slideUp(500);
            });
        }
    })
    event.preventDefault()

}



function pfEdit(event){
    debugger;
    id = event.currentTarget.dataset['pfid'] 
    var dpconf = "";
    var modal = null;
    actionconf = "/printformat/editPF/"+id;
    $("#pfEditModal").on("show.bs.modal", function() {
        if (modal == null) {
            var modal = $.ajax(actionconf)
            
            .done(function(data) {
                $("#pfEditModalBody").html(data);
            })
            
            .fail(function() {
                alert("error");
            });
        }

    });
    $('#pfEditModal').on('hidden.bs.modal', function () {
        $("#pfEditModalBody").modal('hide');
        $(this).data('modal', null);
        $("#pfEditModalBody").html("");
    })

};

function printformatupdate(event){
    debugger;
    id =  event.currentTarget.dataset['pfid'] 
    var formdata = new FormData($("#printformateditform")[0]);
   
    // for (var [key, value] of formdata.entries()) { 
    //     console.log(key, value);
    // }
    $.ajax({
        type:'POST',
        url:"/printformat/editPF/"+id,
        data:formdata,
        processData: false,
        contentType: false, 
        success:function(res){
            debugger
            console.log(res);
            if (res == "TITLE"){
                console.log(res)
                $("#divErrorPFEdit").empty();
                $("#divErrorPFEdit").fadeTo(2000, 500).append("<h4>Alert!</h4>Title already exist.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorPFEdit").slideUp(500);
                });

            }
            else if (res == "Failure"){
                console.log(res)
                $("#divErrorPFEdit").empty();
                $("#divErrorPFEdit").fadeTo(2000, 500).append("<h4>Alert!</h4>Save Failed").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorPFEdit").slideUp(500);
                });

            }

            else if (res == "DO"){
                console.log(res)
                $("#divErrorPFEdit").empty();
                $("#divErrorPFEdit").fadeTo(2000, 500).append("<h4>Alert!</h4>Display Order should be unique.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorPFEdit").slideUp(500);
                });

            }
    
            else if(res == "Success"){
                debugger;
                $("#divResultPFEdit").empty();

                $("#divResultPFEdit").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                    $("#divResultPFEdit").slideUp(500);
                });
                window.location.reload();
            }
           
        },
        error: function(data) {
            debugger
            console.log(data);
            $("#divErrorPFEdit").empty();
                $("#divErrorPFEdit").fadeTo(2000, 500).append("<h4>Alert!</h4>Save Failed").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorPFEdit").slideUp(500);
            });
        }
    })
    e.preventDefault()

};