/*------------------------------------------------------------------------------
 *models function for editbutton in db_profile.html
 *----------------------------------------------------------------------------*/
  $(document).on('click', '#edit_button1',function(e){
    debugger;
    var transactionid = "";
    var dpcon = "";
    var modal = null;
    transactionid =e.currentTarget.attributes['data-transactionid'].value;
    dpcon= '/schema/Editprof/'+transactionid;
    $("#editDbproModal").on("show.bs.modal", function () { 
       setTimeout(function() {
         if (modal == null) {
       modal = $.ajax(dpcon)
           .done(function(data) {
      
               $("#editDbprobody").html(data);
              // $("#modal").modal('show');
           })
           .fail(function() {
               alert("error");
           });
         }},500);
    });

     $('#editDbproModal').on('hidden.bs.modal', function () {
            $("#editDbprobody").modal('hide');
             $(this).data('modal', null);
            $("#editDbprobody").html("");
            });
     });

/*------------------------------------------------------------------------------
 *models function for editbutton in display.html
 *----------------------------------------------------------------------------*/

 $(document).on('click', '#edit_button',function(e){
   debugger;
    var transactionid = "";
    var dpcon ="";
    var modal = null;
    transactionid =e.currentTarget.attributes['data-transactionid'].value;
     dpcon= '/schema/Edit/'+transactionid;
    $("#editDbModal").on("show.bs.modal", function () { 
        setTimeout(function() {
         if (modal == null) {
       modal = $.ajax(dpcon)
           .done(function(data) {
 
               $("#editDbbody").html(data);
             // $("#squarespaceModal").modal('show');
           })
           .fail(function() {
               alert("error");
           });
         }},500);
    });
     $('#editDbModal').on('hidden.bs.modal', function () {
            $("#editDbbody").modal('hide');
             $(this).data('modal', null);
            $("#editDbbody").html("");
            });
     });

/*------------------------------------------------------------------------------
 *models function for add New in display.html
 *----------------------------------------------------------------------------*/
   $(document).on('click', '#addDbprof',function(e){
   debugger;
    var dpcon ="";
    var modal = null;
     dpcon= '/schema/addDb/';
    $("#addDbModal").on("show.bs.modal", function () { 
        setTimeout(function() {
         if (modal == null) {
       modal = $.ajax(dpcon)
           .done(function(data) {
 
               $("#addDbbody").html(data);
             // $("#squarespaceModal").modal('show');
           })
           .fail(function() {
               alert("error");
           });
         }},500);
    });
     $('#addDbModal').on('hidden.bs.modal', function () {
            $("#addDbbody").modal('hide');
             $(this).data('modal', null);
            $("#addDbbody").html("");
            });
     });
