$( document ).ready(function() {
  // Grid or list selection
  $('#btn-list').on('click', function() {
    $('#main-folders').addClass('flex-column');
    $('#btn-grid').removeClass('active')
    $(this).addClass('active')
  });
  $('#btn-grid').on('click', function() {
    $('#main-folders').removeClass('flex-column');
    $('#btn-list').removeClass('active')
    $(this).addClass('active')
  });
  $('#btn-list').on('click', function() {
    $('#main-files').addClass('flex-column');
    $('#btn-grid').removeClass('active')
    $(this).addClass('active')
  });
  $('#btn-grid').on('click', function() {
    $('#main-files').removeClass('flex-column');
    $('#btn-list').removeClass('active')
    $(this).addClass('active')
  });
  
  // Open folder and see files
  // $('button.folder-container').on('click', function() {
  //   $('#filesGroup').removeClass('d-none');
  //   $('#foldersGroup').addClass('d-none')
  // });
});