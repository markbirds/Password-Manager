$(document).ready(function(){ 

    //saving/editing personal information (settings modal)
    $('#save_personal_info').click(function(){
        var id = $('#save_id').val()
        var name = $('#save_name').val().trim()
        var address = $('#save_address').val().trim()
        var age = $('#save_age').val().trim()
        var email = $('#save_email').val().trim()
        var likes_hobbies = $('#save_likes_hobbies').val().trim()
        if(name && address && age && email &&likes_hobbies){
            $.post('/profile/info',{
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
        if(old_pass=='test_password'){
            $('#incorrect_old_pass').text('You cant change this password.');
        }else{
            var new_pass = $('#change_new_pass').val().trim()
            var confirm_pass = $('#change_confirm_pass').val().trim()
            if(old_pass && new_pass && confirm_pass){
                $.post('/profile/confirm_old_pass',{
                old_pass: old_pass
            },function(data){
                if(data['response']){
                    if(new_pass == confirm_pass){
                        $.post('/profile/change_pass',{
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
    }
    });

    //changing background display (settings modal)
    $('#save_display').click(function(){
        var display_number = $('#display_number').val();
        $.post('/profile/background',{
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
        $.post('/profile/mail/report',{
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
            $.post('/profile/mail/suggestion',{
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
    $.post('/api/edit',{
        id: id,
        social_media: social_media,
        username: username,
        password: password
    },function(data,status){
        output = construct_table(data);
        $('#account_body').html(output);
    });
}

//add function (social media information)
function add(){
    var social_media = $('#social_media').val().trim(); 
    var username = $('#username').val().trim(); 
    var password = $('#password').val().trim();
    if(social_media && username && password){
        $.post('/api/add',{
            social_media: social_media,
            username: username,
            password: password
        },function(data,status){
            $('#social_media').val('');
            $('#username').val('');
            $('#password').val('');
            $('#invalid-feedback').text('')
            output = construct_table(data);
            $('#account_body').html(output);
        });
    }else{
        $('#invalid-feedback').text('Please fill out all fields.')
    }
  }; 

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

//function for deleting a social media account information
function delete_account(id){
    $.post('/api/delete',{
        id: id
    },function(data){
        $('#invalid-feedback').text('')
        output = construct_table(data);
        $('#account_body').html(output);
    });
}
