$(document).ready(function()
{
    return;
    var ulnode = $('ul');
    for (i = 1; i < 10; ++i)
        ulnode.append('<li><img src="0' + i + '.jpg"/> <div class = "desp">0' + i+  '.jpg</div></li>' );
    $('ul li').bind('mouseover',function()
    {
        $(this).addClass('selected');
    })
    .bind('mouseout',function()
    {
        $(this).removeClass('selected');
    });

})