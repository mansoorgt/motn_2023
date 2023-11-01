SetupLocationLinks()

function SetupLocationLinks() {
    temp_loc=localStorage.getItem('temp-loc')
    const locationId=temp_loc ? temp_loc : 1
  
    $('.loc-page-link').each(function(){
        let _url = new URL($(this).attr('href'),window.location.origin)
  
        _url.searchParams.set('loc',locationId)
        $(this).attr('href',_url)
        
      })
      console.log($(`[loc-id=${locationId}]`))
      current_location_name=$(`[loc-id=${locationId}]`).text()
      $('.current-location-name').text(current_location_name)
  
}


$('.select-location-option').click(function () {
    let select_loc_id=$(this).attr('loc-id')

    localStorage.setItem('temp-loc',select_loc_id)
    // window.location.href=`${window.location.pathname}?table-name=${table_name}&loc=${select_loc_id}`
    

    let _url = new URL(window.location.href,window.location.origin)
  
    _url.searchParams.set('loc',select_loc_id)
    window.location.href=_url
    
})