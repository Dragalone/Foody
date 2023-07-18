document.addEventListener('click', function(thenew)
{
        var varstyle ;
        the_id    = thenew . target.id;  // console.log(  the_id    );
        the_class = thenew . target.className;

        if(the_class == 'toopen')
        {
          toclose = document.getElementById(the_id);
          toclose .style . display  = 'none';
          name_tag = toclose .tagName;
          if(name_tag =='A')      { varstyle ='inline'; }
          if(name_tag =='BUTTON') { varstyle ='inline-block'; }
          if(name_tag =='SPAN')   { varstyle ='inline'; }
          if(typeof varstyle == 'undefined' && !varstyle){ varstyle ='block'; }
          toopen = document.getElementById(the_id.replace( 'first', 'second'));
          toopen  .style . display  = 'block';
          toopen  .dataset.style    = varstyle  ;
        }
        if(the_class == 'toclose')
        {
          toopen   =  document.getElementById(the_id);
          varstyle = toopen.dataset.style;
          toopen .style . display  = 'none';
          document.getElementById(the_id.replace( 'second', 'first')) .style. display  = varstyle;
        }
});
