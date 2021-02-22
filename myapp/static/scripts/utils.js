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


function construct_table(accounts){
  output="";
  for(var i = 0;i<accounts.length;i++){   
    output += '<tr id="edit_row'+accounts[i]['id'].toString()+'" style="text-align: center;">' +
        '<td id="social_media'+accounts[i]['id'].toString()+'" style="width: 30%;">'+accounts[i]['social_media']+'</td>' +
        '<td id="username'+accounts[i]['id'].toString()+'" style="width: 30%;">'+accounts[i]['username']+'</td>' +
        '<td id="password'+accounts[i]['id'].toString()+'" style="width: 30%;">'+accounts[i]['password']+'</td>' +
        '<td class="p-1" style="width: 5%;text-align: right;">' +
            '<button class="btn btn-warning" id="'+accounts[i]['id'].toString()+'" onclick="edit_account(this.id)">Edit</button>' +
        '</td>' +
        '<td class="p-1" style="width: 5%;">' +
            '<button class="btn btn-danger" id="'+accounts[i]['id'].toString()+'" onclick="delete_account(this.id)">Delete</button>' +
        '</td>' +
    '</tr>';
  }   
  output+=
  '<tr>'+
    '<td class="px-2" style="width: 30%;">'+
      '<input type="text" class="form-control" name="social_media" id="social_media">'+
    '</td>'+
    '<td class="px-2" style="width: 30%;">'+
      '<input type="text" class="form-control" name="username" id="username">'+
      '<div class="text-danger text-center py-3" id="invalid-feedback"></div>'+
    '</td>'+
    '<td class="px-2" style="width: 30%;">'+
      '<input type="text" class="form-control" name="password" id="password">'+
    '</td>'+
    '<td class="px-1" colspan="2">'+
      '<button type="button" class="btn btn-dark px-5" onclick="add()">Add</button>'+
    '</td>'+
  '</tr>';
  return output;
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
