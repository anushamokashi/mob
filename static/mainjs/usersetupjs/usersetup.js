/*------------------------------------------------------------------------------
  *Validation Function for new and edit in usersignup.html and useredit.html
  *----------------------------------------------------------------------------*/

            $('#mail')
               .focusout(function() {
                debugger;
                    var email = $(this).val();
                    console.log(email);
                    ValidateEmail(email);
                    
                    $.ajax({
                         type : 'post',
                         url :'/usersetup/mailValidation/',
                         data : {emailid : email},                 
                         success : function (data) {
                            
                              if(data){
                                   $("#validationmsg").text(data);
                                   setTimeout(function(){
                                        $("#validationmsg").text("");
                                   },6000);
                              }
                         },
                         failure : function (data) {
                              alert('An error occurred.');
                         console.log(data);
                    }
               });
          });
function ValidateEmail(mail) 
  {
  if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(mail))
  {
  return (true)
  }
  $("#validationmsg").empty();
  $("#validationmsg").fadeTo(2000, 500).append("<p>Entered Email Is Invalid One.</p>").slideUp(500, function() {
    $("#validationmsg").slideUp(500);
             });
  return (false)
  }