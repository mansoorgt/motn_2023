var current_id=0
var next_id=0
var previous_id=0
function onProfileClick(id){

    $.ajax({
        type: "GET",
        url: "get-profile-data",
        data: {id:id},
        dataType: "json",
        success: function (response) {
            current_id=id
            $('#profile-modal .profile-content').html(response.html) 
            // $('#profile-modal').modal('show')
            initailSetupProfileview()
            

        }
    });
}

function initailSetupProfileview() {
    
    //setuping next and provious button
    var ListOfRows=$(".reg-tr")
    $('.profile-navigation-btn').addClass('d-none')

    ListOfRows.each( function (i, elm) { 
        var reg_id=$(this).attr('reg-id')
        // console.log(reg_id)
        if (reg_id == current_id && ListOfRows[i+1] ){
            
            next_id=$(ListOfRows[i+1]).attr('reg-id')
            $('.profile-next-btn').removeClass('d-none')
       
        }

        if (reg_id == current_id && ListOfRows[i-1] ){
            
            previous_id=$(ListOfRows[i-1]).attr('reg-id')
            $('.profile-previous-btn').removeClass('d-none')
        
        }
        

    });


    //seutping image view portion of porfile
    const element = document.getElementById('panzoom')
    const panzoom = Panzoom(element, {});
    const parent = element.parentElement
    parent.addEventListener('wheel', panzoom.zoomWithWheel);
   

    //setuting footer approve and reject buttons ( becuse when updating contect of .cetnter doesn't incoude the footer if add the footer in content doesnt work the model close and model functions )
  
    $('.profile-verification-btn').attr('reg-id',current_id)

    


}

function onPreviewImage(elm) {
    $('#profile-preview-img')[0].src=$(elm)[0].src
}

$('.profile-next-btn').click(function(){
    onProfileClick(next_id)
})
$('.profile-previous-btn').click(function(){
    onProfileClick(previous_id)
})

