	    
window.addEventListener('DOMContentLoaded',()=>{
	    console.log('LOADED')
    if (window.location.pathname==='/')
    {fetch('/ideas')
        .then(resp=>resp.json())
        .then(data=>{    
            data.map(idea=>
            display(idea))
        })
        .catch(err=>alert(err))    
    }
       
        $('#add-form').submit(e =>{
            e.preventDefault()
            let title= $('#title-input').val()
            let desc=$('#desc').val()
            let payload={title:title,
                 description:desc
            }
		let action={action:'add',method:'POST'
			}
            hermes(action,payload)

        })

        $('#edit-form').submit(e =>{
            e.preventDefault()
            let id=window.location.pathname.split('/').pop()
            console.log(id)
            let title= $('#edit-title-input').val()
            let desc=$('#edit-desc').val()
            let payload={title:title,
                 description:desc
            }
		let action={action:'edit',method:'PATCH'
			}
            hermes(action,payload,id)
        })
	$('#delete-key').click(()=>{
		console.log('clicked')
	let res=confirm('are you sure')
		if (res){
        let id=window.location.pathname.split('/').pop()
		let action={action:'delete',method:'DELETE'
			}
            hermes(action,'',id)
		}	
	})

    function hermes(actions,payload,id=''){
        let url;
			let {action,method}={...actions}
			switch(action){
            case 'edit':
                url=`/edit/${id}`
                break;
            case 'add':
                url='/add/idea';
               break;
	case 'delete':
		console.log('case delete')
		url=`/delete/${id}`
		break;
	default:
		url=''
        }
        fetch(url,{
			method:method,
            mode:'cors',
            headers:{
            'Content-Type':'application/json'
            },
            body:JSON.stringify(payload) 
        })
        .then(resp=>resp.json())
        .then(data=>{console.log('DATA:',data)
            alert(data.message)
            })
        .catch(err=>{alert(err)})
    }


const display = (data, index) => {
    let container = $('#ideas-container')
    let idea= document.createElement('div');
    let title=document.createElement('h3')
    let preview_desc=document.createElement('p')
    let date = document.createElement('span')
    let link=document.createElement('a')
    link.href=`/idea/${data.id}`
    date.innerHTML = data.date
    title.innerHTML = data.title
    preview_desc.innerHTML = data.description.slice(0,20)
    link.appendChild(title)
    idea.appendChild(link)
    idea.appendChild(preview_desc)
    idea.append(date);
    date.className +='date';
    idea.className += 'idea';

    container.append(idea);


}
})
