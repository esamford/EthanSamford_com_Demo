/*
    VS Code doesn't like the following code:
        <* style="background-image: url(' {% static 'source' %} ');"></*>

    It works fine, but it won't stop telling me there's a problem to fix.

    To prevent myself from accidentally breaking something later, I've added
    some jQuery code that will write this for me. Just add the "data-background-src"
    tag to the element with a background image, and place the URL inside.
*/

$(document).ready(function() {
    $('[data-background-src]').each(function() {
        let image_src = $(this).attr('data-background-src');
        $(this).css('background-image', "url('" + image_src + "')");
        $(this).removeAttr('data-background-src')
    });
});