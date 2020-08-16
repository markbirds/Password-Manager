//animation on login
function onload_page(){
    if($(window).width()>500){
    $("#password_manager, #password_login").animate({'margin-top': '10%'},1000);
    }
}

// Add the following code if you want the name of the file appear on select
$(".custom-file-input").on("change", function() {
  var fileName = $(this).val().split("\\").pop();
  $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
});

//setting the border for saved display in display settings
var display_number = $('#display_number').val();
var bg_key = ["background-image","background-color","background-color","background-color"];
var bg_value = ["linear-gradient(90deg, #97d5c8 ,#5b6e7f)","#a3c2b3","#bfbfbf","#f5ae71"];
for(var i=1;i<=4;i++){
    if(i!=display_number){
        $('#display_box'+i.toString()).css({'border':'5px solid white'});
        continue;
    }
    $('#display_box'+i.toString()).css({'border':'5px solid #363535'}); 
    $('#body').css(bg_key[display_number-1],bg_value[display_number-1]);

}

//responsive format 
function body_responsive(accounts){
    output = ""
    for(var i = 0;i<accounts.length;i++){
        output+=
    '<div id=edit_row'+accounts[i].id+'>'+
        '<table class="table table-striped table-hover">'+
            '<tr>' +
                '<th style="width: 40%;">Social Media</th>' + 
                '<td id=social_media'+accounts[i].id+'>'+accounts[i].social_media+'</td>' +
            '</tr>' +
            '<tr>' +
                '<th style="width: 40%;">Username</th>' + 
                '<td id=username'+accounts[i].id+'>'+accounts[i].username+'</td>' +
            '</tr>' +
            '<tr>' +
                '<th style="width: 40%;">Password</th>' + 
                '<td id=password'+accounts[i].id+'>'+accounts[i].password+'</td>' +
            '</tr>' +
        '</table>' +
        '<div class="clearfix mb-3">' +
            '<div class="float-left">' +
                '<button class="btn btn-warning mx-1" onclick='+accounts[i].edit_account_responsive+'>Edit</button>' +
            '</div>' +
            '<div class="float-left">' +
                '<button class="btn btn-danger mx-1" onclick='+accounts[i].delete_account_responsive+'>Delete</button>' +
            '</div>' +
        '</div>' +
    '</div>';
    }
    output+=
    '<hr>'+
        '<table>' +
            '<tr>' +
                '<th style="width: 40%;">Social Media</th>' +
                '<td>' +
                    '<input type="text" class="form-control" name="social_media" id="social_media">' +
                    '<div class="invalid-feedback"></div>' +
                '</td>' +
            '</tr>' +
            '<tr>' +
            '<th>Username</th>' +
                '<td>' +
                    '<input type="text" class="form-control" name="username" id="username">' +
                '</td>' +
                '</tr>' +
            '<tr>' +
            '<th>Password</th>' +
                '<td>' +
                    '<input type="text" class="form-control" name="password" id="password">' +
                '</td>' +
                '</tr>' +
            '<tr>' +
            '<tr>' +
                '<td></td>'+
                '<td>' +
                    '<div class="text-danger text-center py-3" id="invalid-feedback"></div>' +
                '</td>' +
                '</tr>' +
            '<tr>' +
                '<td></td>'+
                '<td class="pt-3 text-right">' +
                    '<button type="button" class="btn btn-dark px-5" id="add" onclick="add_responsive()">Add</button>' +
                '</td>' +
                '</tr>' +
        '</table>';
    return output;
}

$(document).ready(function(){ 
    //checks of the window width is less than 500   
    //requests for data and formats the dashboard in responsive style
    if($(window).width()<500){
        $.get('/responsive',function(data,status){
            accounts = JSON.parse(data);   
            $('#card_responsive').html(body_responsive(accounts));
        });
    }
    //resize event for responsive style
    $(window).resize(function(){
        if($(window).width()<500){
        $.get('/responsive',function(data,status){
            accounts = JSON.parse(data);   
            $('#card_responsive').html(body_responsive(accounts));
        });
    }
    });

    //add function (social media information)
    $('#add').click(function(){
        var social_media = $('#social_media').val().trim(); 
        var username = $('#username').val().trim(); 
        var password = $('#password').val().trim();
        if(social_media && username && password){
            $.post('/accounts',{
                social_media: social_media,
                username: username,
                password: password
            },function(data,status){
                $('#social_media').val('');
                $('#username').val('');
                $('#password').val('');
                $('#invalid-feedback').text('')
                accounts = JSON.parse(data);
                output="";
                for(var i = 0;i<accounts.length;i++){   
                output += '<tr id="edit_row'+accounts[i]['id'].toString()+'" style="text-align: center;">' +
                    '<td id="social_media'+accounts[i]['id'].toString()+'" style="width: 30%;">'+accounts[i]['social_media']+'</td>' +
                    '<td id="username'+accounts[i]['id'].toString()+'" style="width: 30%;">'+accounts[i]['username']+'</td>' +
                    '<td id="password'+accounts[i]['id'].toString()+'" style="width: 30%;">'+accounts[i]['password']+'</td>' +
                    '<td class="p-1" style="width: 5%;text-align: right;">' +
                        '<button class="btn btn-warning" onclick="edit_account('+accounts[i]['id'].toString()+')">Edit</button>' +
                    '</td>' +
                    '<td class="p-1" style="width: 5%;">' +
                        '<button class="btn btn-danger" onclick="delete_account('+accounts[i]['id'].toString()+')">Delete</button>' +
                    '</td>' +
                '</tr>';
                }     
                $('#account_body').html(output);
            });
        }else{
            $('#invalid-feedback').text('Please fill out all fields.')
        }
    }); 
    //saving/editing personal information (settings modal)
    $('#save_personal_info').click(function(){
        var id = $('#save_id').val()
        var name = $('#save_name').val().trim()
        var address = $('#save_address').val().trim()
        var age = $('#save_age').val().trim()
        var email = $('#save_email').val().trim()
        var likes_hobbies = $('#save_likes_hobbies').val().trim()
        if(name && address && age && email &&likes_hobbies){
            $.post('/personal_info',{
                id: id,
                name: name,
                address: address,
                age: age,
                email: email,
                likes_hobbies: likes_hobbies
            },function(status){
                console.log(status);
                $('#account_saved').text('Account saved.')
            });
        }
    });
    //changing password (settings modal)
    $('#change_pass').click(function(){
        var old_pass = $('#change_old_pass').val().trim()
        var new_pass = $('#change_new_pass').val().trim()
        var confirm_pass = $('#change_confirm_pass').val().trim()
        if(old_pass && new_pass && confirm_pass){
            $.post('/confirm_old_pass',{
            old_pass: old_pass
        },function(data){
            if(JSON.parse(data)['response']){
                if(new_pass == confirm_pass){
                    $.post('/change_pass',{
                        new_pass: new_pass
                    },function(status){
                        console.log(status);
                        $('#not_match').text('')
                        $('#incorrect_old_pass').text('')
                        $('#pass_changed').text('Password successfully changed.')
                    })
                }else{
                    $('#not_match').text('Passwords dont match.');
                }
            }else{
                $('#incorrect_old_pass').text('Incorrect Password.');
            }
        });
    }
    });
    //changing background display (settings modal)
    $('#save_display').click(function(){
        var display_number = $('#display_number').val();
        $.post('/save_display',{
            display_number: display_number
        },function(status){
            $('#display_saved').text('Display saved.');
        });
        var bg_key = ["background-image","background-color","background-color","background-color"];
        var bg_value = ["linear-gradient(90deg, #97d5c8 ,#5b6e7f)","#a3c2b3","#bfbfbf","#f5ae71"];
        $('#body').css(bg_key[display_number-1],bg_value[display_number-1]);
    });

    //sending problem (settings modal)
    $('#report_send').click(function(){
        var report = $('#report_textarea').val().trim();
        var name = $('#save_name').val().trim()
        if(report){
        $('#report_textarea').val('');
        $('#report_sent').html('<button class="btn btn-danger">'+
                                    '<span class="spinner-border spinner-border-sm"></span>'+
                                    ' Sending report. Please wait.'+
                                '</button>');
        $('#report_sent').addClass('py-3 text-center');     
        $.post('/mail/report',{
            name: name,
            report: report
        },function(){
            $('#report_sent').html('<button class="btn btn-success">'+
                                        'Report sent'+
                                    '</button>');
        });
        }
    });
    //sending suggestions (settings modal)
    $('#suggestion_send').click(function(){
        var suggestion = $('#suggestion_textarea').val().trim();
        var name = $('#save_name').val().trim()
        if(suggestion){
        $('#suggestion_textarea').val('');
        $('#suggestion_sent').html('<button class="btn btn-danger">'+
                                    '<span class="spinner-border spinner-border-sm"></span>'+
                                    ' Sending suggestion. Please wait.'+
                                '</button>');
        $('#suggestion_sent').addClass('py-3 text-center');
            $.post('/mail/suggestion',{
                name: name,
                suggestion: suggestion
            },function(){
                $('#suggestion_sent').html('<button class="btn btn-success">'+
                                            'Suggestion sent'+
                                        '</button>');
            });
        }
    });
    // link in footer --> navigates into report section in settings modal
    $('#footer_suggestion').click(function(){
        $('#report_link').click();
    });
});

//function for displaying border in each display box once clicked
function select_display(num){
var bg_key = ["background-image","background-color","background-color","background-color"];
var bg_value = ["linear-gradient(90deg, #97d5c8 ,#5b6e7f)","#a3c2b3","#bfbfbf","#f5ae71"];
    for(var i=1;i<=4;i++){
        if(i!=num){
            $('#display_box'+i.toString()).css({'border':'5px solid white'});
            continue;
        }
    $('#display_box'+i.toString()).css({'border':'5px solid #363535'}); 
    var display_number = $('#display_number').val(num);
    }    
}

//function for saving the edited social media information in the dashboard
function confirm(id){
    social_media = $('#edit_social_media'+id.toString()).val()
    username = $('#edit_username'+id.toString()).val()
    password = $('#edit_password'+id.toString()).val()
    $.post('/edit',{
        id: id,
        social_media: social_media,
        username: username,
        password: password
    },function(data,status){
        accounts = JSON.parse(data);
        output="";
        for(var i = 0;i<accounts.length;i++){   
        output += '<tr id="edit_row'+accounts[i]['id'].toString()+'" style="text-align: center;">' +
            '<td id="social_media'+accounts[i]['id'].toString()+'" style="width: 30%;">'+accounts[i]['social_media']+'</td>' +
            '<td id="username'+accounts[i]['id'].toString()+'" style="width: 30%;">'+accounts[i]['username']+'</td>' +
            '<td id="password'+accounts[i]['id'].toString()+'" style="width: 30%;">'+accounts[i]['password']+'</td>' +
            '<td class="p-1" style="width: 5%;text-align: right;">' +
                '<button class="btn btn-warning" onclick="edit_account('+accounts[i]['id'].toString()+')">Edit</button>' +
            '</td>' +
            '<td class="p-1" style="width: 5%;">' +
                '<button class="btn btn-danger" onclick="delete_account('+accounts[i]['id'].toString()+')">Delete</button>' +
            '</td>' +
        '</tr>';
        }     
        $('#account_body').html(output);
    });
}

//function for converting the table data into input fields
function edit_account(id){
    var social_media = $("#social_media"+id.toString()).text()
    var username = $("#username"+id.toString()).text()
    var password = $("#password"+id.toString()).text()
    output = 
    '<td class="px-2" style="width: 30%;">' +
        '<input type="text" class="form-control" name="edit_social_media'+ id.toString()+ '" id="edit_social_media'+ id.toString()+ '" value="'+ social_media +'">'  +
    '</td>'+
    '<td class="px-2" style="width: 30%;">'+
        '<input type="text" class="form-control" name="edit_username'+ id.toString()+ '" id="edit_username'+ id.toString()+ '" value="'+ username +'">' +
    '<td class="px-2" style="width: 30%;">' +
        '<input type="text" class="form-control" name="edit_password'+ id.toString()+ '" id="edit_password'+ id.toString()+ '"value="'+ password +'">' +
    '</td>' +
    '<td class="p-1" style="width: 5%;text-align: right;">' +
        '<button class="btn btn-warning mt-2" onclick=confirm('+id.toString()+')>Edit</button>' +
    '</td>' +
    '<td class="p-1" style="width: 5%;">' +
        '<button class="btn btn-danger mt-2" onclick=delete_account('+id.toString()+')>Delete</button>'+
    '</td>';
    $("#edit_row"+id.toString()).html(output);
}

//function for deleting an social media account information
function delete_account(id){
    $.post('/delete',{
            id: id
        },function(data){
            $('#invalid-feedback').text('')
            output="";
            accounts = JSON.parse(data);
            for(var i = 0;i<accounts.length;i++){            
                output += '<tr id="edit_row'+accounts[i]['id'].toString()+'" style="text-align: center;">' +
                '<td id="social_media'+accounts[i]['id'].toString()+'" style="width: 30%;">'+accounts[i]['social_media']+'</td>' +
                '<td id="username'+accounts[i]['id'].toString()+'" style="width: 30%;">'+accounts[i]['username']+'</td>' +
                '<td id="password'+accounts[i]['id'].toString()+'" style="width: 30%;">'+accounts[i]['password']+'</td>' +
                '<td class="p-1" style="width: 5%;text-align: right;">' +
                    '<button class="btn btn-warning" onclick="edit_account('+accounts[i]['id'].toString()+')">Edit</button>' +
                '</td>' +
                '<td class="p-1" style="width: 5%;">' +
                    '<button class="btn btn-danger" onclick="delete_account('+accounts[i]['id'].toString()+')">Delete</button>' +
                '</td>' +
            '</tr>';
            }    
            $('#account_body').html(output);
        });
}

//function to add social media information --> triggered when in responsive style
function add_responsive(){
    var social_media = $('#social_media').val().trim(); 
    var username = $('#username').val().trim(); 
    var password = $('#password').val().trim();
    if(social_media && username && password){
        $.post('/accounts',{
            social_media: social_media,
            username: username,
            password: password
        },function(data,status){
            $('#social_media').val('');
            $('#username').val('');
            $('#password').val('');
            $('#invalid-feedback').text('')
            accounts = JSON.parse(data);
            $('#card_responsive').html(body_responsive(accounts));
        });
    }else{
        $('#invalid-feedback').text('Please fill out all fields.')
    }    
}

//function to delete social media information --> triggered when in responsive style
function delete_account_responsive(id){
    $.post('/delete',{
            id: id
        },function(data){
            $('#invalid-feedback').text('')
            output="";
            accounts = JSON.parse(data);
            $('#card_responsive').html(body_responsive(accounts));
        });
}

//function to confirm edited social media information --> triggered when in responsive style
function confirm_responsive(id){
    social_media = $('#edit_social_media'+id.toString()).val()
    username = $('#edit_username'+id.toString()).val()
    password = $('#edit_password'+id.toString()).val()
    $.post('/edit',{
        id: id,
        social_media: social_media,
        username: username,
        password: password
    },function(data,status){
        accounts = JSON.parse(data);
        $('#card_responsive').html(body_responsive(accounts));
    });
}

//function to edit social media information --> triggered when in responsive style
//converts the table data into input fields
function edit_account_responsive(id){
    var social_media = $("#social_media"+id.toString()).text()
    var username = $("#username"+id.toString()).text()
    var password = $("#password"+id.toString()).text()
    output =
    '<table class="table table-striped table-hover">'+
    '<tr>' +
        '<th style="width: 40%;">Social Media</th>' + 
        '<td><input type="text" class="form-control" name="edit_social_media'+ id.toString()+ '" id="edit_social_media'+ id.toString()+ '" value="'+ social_media +'"></td>' +
    '</tr>' +
    '<tr>' +
        '<th style="width: 40%;">Username</th>' + 
        '<td><input type="text" class="form-control" name="edit_username'+ id.toString()+ '" id="edit_username'+ id.toString()+ '" value="'+ username +'"></td>' +
    '</tr>' +
    '<tr>' +
        '<th style="width: 40%;">Password</th>' + 
        '<td><input type="text" class="form-control" name="edit_password'+ id.toString()+ '" id="edit_password'+ id.toString()+ '"value="'+ password +'"></td>' +
    '</tr>' +
    '</table>'+
    '<div class="clearfix mb-3">' +
            '<div class="float-left">' +
                '<button class="btn btn-warning mx-1" onclick=confirm_responsive('+id.toString()+')>Edit</button>' +
            '</div>' +
            '<div class="float-left">' +
                '<button class="btn btn-danger mx-1" onclick=delete_account_responsive('+id.toString()+')>Delete</button>' +
            '</div>' +
    '</div>';
    $("#edit_row"+id.toString()).html(output);
}

// Disable form submissions if there are invalid fields
(function() {
  'use strict';
  window.addEventListener('load', function() {
    // Get the forms we want to add validation styles to
    var forms = document.getElementsByClassName('needs-validation');
    // Loop over them and prevent submission
    var validation = Array.prototype.filter.call(forms, function(form) {
      form.addEventListener('submit', function(event) {
        if (form.checkValidity() === false) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      }, false);
    });
  }, false);
})();
