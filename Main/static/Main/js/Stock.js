// Stock_read_items.html
function isDelete(num){
    if(confirm("정말 삭제하시겠습니까?"))
    {
        var url = "/Stock/"+num+"/Delete/"
        $("form[name='delete']").attr("action", url);
        $("form[name='delete']").submit();
    }
}

// Order_read_items.html
function o_isDelete(num)
{
    if(confirm("정말 삭제하시겠습니까?"))
    {
        var url = "/Order/"+num+"/Delete/"
        $("form[name='delete']").attr("action", url);
        $("form[name='delete']").submit();
    }
}