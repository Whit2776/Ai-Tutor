// HTML Class Nmaes
let chat_linkEl_id = 'chat-link'
let user_idEl_id = 'id'
let messages_containerEl_class = '.messages-container'
let add_files_iconEl_id = '.add-files-icon'
let add_files_inputEl_id = '.add-files-input'
let preview_containerEl_class = '.files-preview-container'
let preview_class = '.files-preview'
let formEl_id = 'post-message'
let delete_multipleEl_class = '.delete-multiple'
let message_bubbleEl_class = '.message-wrapper'
let other_user_mesEl_class = '.other-user'

let chat_link = document.getElementById(chat_linkEl_id).innerText
let user_id = Number(document.getElementById(user_idEl_id).innerText)
let messages_container = document.querySelector(messages_containerEl_class)

let add_files_icon = document.querySelector(add_files_iconEl_id)
let add_files_input = document.querySelector(add_files_inputEl_id)
let preview_container = document.querySelector(preview_containerEl_class)
let preview = document.querySelector(preview_class)

let form = document.getElementById(formEl_id)
let delete_multiple = document.querySelector(delete_multipleEl_class)

const bubble = document.querySelector(message_bubbleEl_class)

let get_messages_url = `/chat-api/get-messages/${chat_link}/10`
let get_message_url = `/chat-api/get-message/${chat_link}`
document.querySelector('.chat-info').onclick = () => {
  document.body.classList.toggle('show-profile')
}
const get_messages = async () => {
  let res = await fetch(get_messages_url)
  let data = await res.json()

  return data
}


const render_messages = async () => {
  let data = await get_messages()
  data.data.forEach(message => {
    select_element(message, data.data, data.is_group, message.files)
  })
  scrollToBottom()
}


let messagesEl_class = '.message-wrapper'
let message_idEl_class = '.id'
let message_stateEl_class = '.state'

const get_message = async () => {
  let res = await fetch(get_message_url)
  let data = await res.json()
  console.log(data)

  if(data.data){
    messages = await get_messages()
    select_element(data.data, messages.data, data.is_group, data.data.files)
    scrollToBottom()
  }
}

let send_iconEl_class = '.send'
let submit_formEl_class = '.submit-form'

let post_message_url = `/chat-api/post-message/${chat_link}`

let send_icon = document.querySelector(send_iconEl_class)
let submit_btn = document.querySelector(submit_formEl_class)

const post_message = () => {

  form.addEventListener('submit', async e => {
    e.preventDefault()
    let formdata = new FormData(form)
    let res = await fetch(post_message_url, {method:'post', body:formdata})
    let data = await res.json()

    if(res.ok ){
      form.reset()
      preview.innerHTML = ''
      scrollToBottom()
  
      let r = document.querySelector('.reply-preview')
      if(r) document.querySelector('.reply-preview').remove()
      
      try{window.parent.moveChatToTop(chat_link)}catch(e){console.error(e)}
    }
  })
}

const attach_preview_files = () => {

  add_files_icon.onclick = () => {
    add_files_input.click()
  }

  add_files_input.addEventListener('change', e => {
    let files = Array.from(e.target.files)
    files.length>0 ? preview_container.classList.add('active'):preview_container.classList.remove('active')
    files.forEach(file => {
      let path = URL.createObjectURL(file)
      let type = file.type

      if(type.includes('image')){
        let div = document.createElement('div')
        let img = document.createElement('img')

        img.src = path
        img.classList.add('image')

        div.appendChild(img)
        preview.appendChild(div)
      }
    })
  })
}


const select_element = (message, messages, is_group = false, files) => {
  if(message.sender === user_id){
    let node = bubble.cloneNode(true)
    node.classList.add('sent')
    render_message(messages_container, node, message, files, messages, is_group)
  } else{
    let node = bubble.cloneNode(true)
    node.classList.add('received')
    render_message(messages_container, node, message, files, messages, is_group)
  }
}

const scrollToBottom = () => {
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      messages_container.scrollTop = messages_container.scrollHeight;
    });
  });
};

window.addEventListener('click', e => {
  if (e.target.classList.contains('modal')) e.target.classList.remove('active')
})

let allow_click_on_mes = false


  
let input = document.createElement('input')

let forward_message_slide_in = document.getElementById('forward-message-modal')
let forward_form = forward_message_slide_in.querySelector('#forward-messages')

const forward_message = (message) => {
  forward_message_slide_in.classList.add('active')
  input.name = 'message-id'
  input.type = 'hidden'
  input.value = message.id

  forward_form.appendChild(input)
  forward_message_slide_in.querySelector('.close-btn').onclick = () => {
    forward_message_slide_in.classList.remove('active')
  }

  let forward_chats = forward_message_slide_in.querySelector('.forward-chats')
  Array.from(forward_message_slide_in.querySelectorAll('.name')).forEach(name => {
    let link = name.getAttribute('data-link')
    let inp = document.createElement('input')
    name.onclick = () => {
      name.classList.toggle('highlight')
      if(Array.from(forward_form.children).find(r => {return r.value === link})){
        inp.remove()
        return
      }

      inp.name = 'chat'
      inp.type = 'hidden'
      inp.value = link
      inp.classList.add('hibigitis')
      forward_form.appendChild(inp)
    }
  })
}

const submit_forward_form = () => {
  forward_form.addEventListener('submit', async e =>{
    e.preventDefault()
    let formdata = new FormData(forward_form)
    let res = await fetch(post_message_url, {method:'post', body:formdata})
    let data = await res.json()

    if(res.ok){
      Array.from(forward_form.querySelectorAll('.hibigitis')).forEach(g => {g.remove()})
      Array.from(forward_message_slide_in.querySelectorAll('.name')).forEach(name => {
        name.classList.remove('highlight')
      })
      forward_message_slide_in.classList.toggle('active')
    } else{
      console.error(data.type, data.message)
    }
  })
}

let carousel_card = document.querySelector('.carousel-card')
let modal = document.querySelector('#my-modal')
let cards_container = document.querySelector('.cards')

const render_message = async (container, element, message, files, messages, is_group) => {
  if (is_group) {if(message.sender != user_id)element.querySelector('.sender').textContent = message.sender_name}
  
  if(message.type === 'system'){
    let span = document.createElement('span')
    span.textContent = message.message
    span.classList.add('system')
    container.appendChild(span)
    return
  }

  drag(element, message, form)

  element.querySelector('.message').textContent = message.message
  element.querySelector('.time-stamp').textContent = new Date(message.created).toDateString()
  element.querySelector('.read-status').textContent = '✓'
  element.querySelector(message_idEl_class).textContent = message.id


  element.querySelector('.forward-icon').addEventListener('click', e => { forward_message(message) })
  

  if(files.length > 0){
    let i = 0

    let files_container = document.createElement('div')
    files_container.classList.add('files')

    files.forEach(file => {
      if(file.type.includes('image') && i<3){
        console.log(file)
        let img = document.createElement('img')

        img.src = file.path
        img.classList.add('file')
        files_container.appendChild(img)
      }

      if(i === 3){
        let g = document.createElement('span')
        g.classList.add('remaining-files')
        g.innerText = `+${files.length-3}`
        files_container.appendChild(g)
        return
      }
      i++
    })
    element.querySelector('.message-container').prepend(files_container)
    

    files_container.onclick = () => {
      let cont_id = Number(cards_container.dataset.id)

      
      if(cont_id === message.id){
        modal.classList.add('active')
        return
      }

      cards_container.querySelectorAll('.card').forEach(c => c.remove())
      cards_container.setAttribute('data-id', message.id)
      files.forEach(file => {
        let card = carousel_card.cloneNode(true)
        card.querySelector('.image').src = file.path
        cards_container.appendChild(card)
      })
      add_events(cards_container)
      modal.classList.add('active')
    }
  }

  console.log(messages)

  if(message.type === 'reply'){
    let replyEL = document.createElement('div')

    let reply_to = messages.find(m => {return m.id === message.reply_to})
    
    replyEL.classList.add('reply')

    replyEL.innerText = reply_to.message

    element.prepend(replyEL)
  }
  if(message.type === 'forward'){
    let forwardEl = document.createElement('span')
    forwardEl.classList.add('text-muted')
    forwardEl.textContent = 'Forwarded'
    element.querySelector('.message-container').prepend(forwardEl)
  }

  
  longPress(element, () => {
    allow_click_on_mes = true
    console.log('Long Pressed')
    // append_to_delete(clone, slide_in_form)
    // delete_multiple.parentElement.style.display = 'block'
  })


  container.appendChild(element)
}

const drag = (target, message, form) => {
  let dragging = false
  let startX = 0;
  let currentX = 0;

  let reply_icon = target.querySelector('.reply-icon')
  let forward_icon = target.querySelector('.forward-icon')
  let delete_icon = target.querySelector('.delete-icon')

  target.addEventListener('pointerdown', e => {
    if(e.target.classList.contains('message') || e.target.classList.contains('message-stamp')){
      startX = e.clientX

      if(e.clientX>3)dragging = true

      target.querySelector('.message-container').style.cursor = 'grabbing'
      
      target.style.transition = 'none';
      target.setPointerCapture(e.pointerId);
    }
  })

  let REPLY_THRESHOLD =-30
  let FORWARD_THRESHOLD = 80
  let DELETE_THRESHOLD = 80

  target.addEventListener('pointermove', e => {
    if(!dragging) return
    currentX = e.clientX - startX
    currentX = Math.max(-120, Math.min(100, currentX));
    target.style.transform = `translateX(${currentX}px)`;
    let r_pre = document.querySelector('.reply-preview')

    if(currentX<=REPLY_THRESHOLD){
      
      reply_message(message, target, form)

      reply_icon.classList.add('active')
      forward_icon.classList.remove('active')
      delete_icon.classList.remove('active')
    } else if(currentX<=FORWARD_THRESHOLD){
      forward_icon.classList.add('active')
      reply_icon.classList.remove('active')
      delete_icon.classList.remove('active')
      if(r_pre){
        reset_reply_form(form, r_pre)
      }
    } else if(currentX>DELETE_THRESHOLD){
      forward_icon.classList.remove('active')
      delete_icon.classList.add('active')
      reply_icon.classList.remove('active')
      // if(r_pre){
      //   r_pre.classList.add('disappear')
      //   setTimeout(() => {r_pre.remove()}, 300)
      // }
    }

  })

  target.addEventListener('pointerup', e => {
    dragging = false
    target.style.transition = 'transform 0.2s ease';
    if (currentX > 30) {
      console.log('Forward to??')
    } else if (currentX < -30) {
      console.log('Reply?')
    } 
    reply_icon.classList.remove('active')
    forward_icon.classList.remove('active')
    delete_icon.classList.remove('active')
    target.style.transform = 'translateX(0)';
  })
  function reset() {
    dragging = false;
    target.style.transition = 'transform 0.2s ease';
    target.style.transform = 'translateX(0)';
    reply_icon.classList.remove('active');
    forward_icon.classList.remove('active');
    delete_icon.classList.remove('active');
  }

  target.addEventListener('pointercancel', reset);
  target.addEventListener('pointerleave', reset);
}

document.addEventListener('click', e => {
  let target = e.target
  if(target.classList.contains('my-modal') || target.classList.contains('card')){
    modal.classList.remove('active')
  }
})

let slide_in_form = document.querySelector('.slide-in-form')

const append_to_delete = (element, form) => {
  let delete_message = document.createElement('div')
  let input = document.createElement('input')
  input.name = 'ids'
  input.type = 'hidden'
  input.value = element.querySelector('.id').innerText
  input.id = `ID${element.querySelector('.id').innerText}`
  input.classList.add('input')

  delete_message.innerText = element.querySelector('.actual').innerText
  delete_message.classList.add(`ID${element.querySelector('.id').innerText}`)
  delete_message.classList.add('delete-message')
  
  if(element.querySelector('.chat-box').classList.contains('selected')){
    element.querySelector('.chat-box').classList.remove('selected')
    slide_in.querySelector(`.ID${element.querySelector('.id').innerText}`).remove()
    form.querySelector(`#ID${element.querySelector('.id').innerText}`).remove()
  } else{
    element.querySelector('.chat-box').classList.add('selected')
    slide_in.querySelector('.delete-messages').appendChild(delete_message)
    form.appendChild(input)
  }
}

slide_in_form.addEventListener('submit', async e => {
  e.preventDefault()
  let url = '/chat-api/delete-message'
  let formdata = new FormData(slide_in_form)
  let res = await fetch(url, {method: 'POST', body:formdata})
  let data = await res.json()

  let delete_messages_container = slide_in.querySelector('.delete-messages')
  let inputs = slide_in_form.querySelectorAll('.input')
  let messages = Array.from(document.querySelectorAll('.mes'))

  if(res.ok){
    delete_multiple.style.display = 'none'
    delete_messages_container.innerHTML = ''
    slide_in.classList.remove('active')
    allow_click_on_mes = false
    inputs.forEach( input => {
      messages.find(mes => {return mes.querySelector('.id').innerText === input.value}).remove()
    })
  }
})

let i = 0

document.addEventListener('click', e => {
  let target = e.target
  if (!target.classList.contains('chat-box')) return
  if (allow_click_on_mes && i > 0){
    append_to_delete(target.parentElement, slide_in_form)
    if(!document.querySelector('.delete-message') ){
      i = -1
      allow_click_on_mes = false
      delete_multiple.parentElement.style.display = 'none'
    }
  }

  i++
})
let number = 0
let previous_id = 0
const reply_message = (message, chat_container, message_form) => {
  const r = document.querySelectorAll('.reply-preview')
  const new_id =message.id
  Array.from(r).forEach(e => {
    let id = Number(e.dataset.id)
    if(id === new_id) return
    e.classList.add('disapear')
    setTimeout(() => {e.remove()}, 400)
  })

  if(previous_id != new_id){
    number = 0
    previous_id = new_id
  }

  if(number>0 ){
    return
  }
  
  let m_t = message_form.querySelector('#message-type')
  let rti = message_form.querySelector('#reply-to-id')
  let reply_preview = document.createElement('div')
  let p = document.createElement('div')
  let c = document.createElement('span')


  reply_preview.dataset.id = message.id

  
  c.classList.add('close-btn')

  m_t.value = 'reply'
  rti.value = message.id

  reply_preview.classList.add('reply-preview')
  reply_preview.appendChild(p)
  reply_preview.appendChild(c)
  document.querySelector('.reply-wrapper').prepend(reply_preview)
  p.innerText = `You are replying to: \n ${message.message}`

  c.onclick = () => {
    m_t.value = ''
    reply_preview.classList.add('disapear')
    setTimeout(() => {reply_preview.remove()}, 400)
    number = 0
    previous_id = 0
  }
  number++
}

const reset_reply_form = (message_form, reply_preview) => {
    let m_t = message_form.querySelector('#message-type')
    m_t.value = ''
    reply_preview.classList.add('disapear')
    setTimeout(() => {reply_preview.remove()}, 400)
    number = 0
    previous_id = 0

}

const add_events = (container) => {
  const panels = [...container.querySelectorAll('.card')];
  const btnLeft = container.querySelector('.left');
  const btnRight = container.querySelector('.right');

  function getCurrentIndex(){
    const scrollLeft = container.scrollLeft;
    const width = container.clientWidth;
    let index=  Math.round(scrollLeft / width)
    return index
  }

  function updateButtons(){
    const index = getCurrentIndex();
    index === 0? btnLeft.classList.add('disabled'): btnLeft.classList.remove('disabled');
    index === panels.length - 1? btnRight.classList.add('disabled'): btnRight.classList.remove('disabled');
  }

  btnRight.addEventListener('click', () => {
    const next = Math.min(getCurrentIndex() + 1, panels.length - 1);
    panels[next].scrollIntoView({ behavior: 'smooth', inline: 'start' });
  });

  btnLeft.addEventListener('click', () => {
    const prev = Math.max(getCurrentIndex() - 1, 0);
    panels[prev].scrollIntoView({ behavior: 'smooth', inline: 'start' });
  });

  container.addEventListener('scroll', updateButtons);

  updateButtons();
}

const select_chats = () => {
  let chat_containers = document.querySelectorAll('.chat-wrapper')
  // let form = document.querySelector('.forward-message-form')

  Array.from(chat_containers).forEach(cC => {
    cC.onclick = () => {
      let is_selected = cC.classList.contains('selected')
      let chat_input = document.createElement('input')
      let link = cC.querySelector('.link').innerText
      chat_input.classList.add(`a${link}`)
      if(is_selected){
        cC.classList.remove('selected')
        form.querySelector(`.a${link}`).remove()
      } else{
        chat_input.type = 'hidden'
        chat_input.name = 'chat'
        chat_input.value = link
        form.appendChild(chat_input)
        cC.classList.add('selected')
      }

    }
  })
  
  // let url = `/chat-api/post-message/${chat_link}`

  // form.addEventListener('submit', async e => {
  //   e.preventDefault()
  //   let formdata = new FormData(form)
  //   let res = await fetch(url, {method:'post', body:formdata})
  //   let data = await res.json()})
}

const search_through =  () => {
  let value = document.querySelector('.search').value
  let chats = document.querySelector('.chats')
  let chats_containers = document.querySelectorAll('.chat-container')

  if(value === ''){
    chats_containers.forEach(chat => {
      chat.style.display = 'flex'
  })
    return
  }
  
  chats_containers.forEach(chat => {
    chat.style.display = 'none'
  })

  
  new_chats = Array.from(chats_containers).filter(chat => {return chat.querySelector('.name').innerText.toLowerCase().includes(value.toLowerCase())})

  new_chats.forEach(c => {
    c.style.display = 'flex'
    chats.prepend(c)
  })

}

document.querySelector('.search').addEventListener('input', e => {
  search_through()
})


let event_is_active = true

function longPress(target, callback, duration = 600) {
  let timer;

  target.addEventListener("mousedown", () => {
    if(!event_is_active) return
    timer = setTimeout(callback, duration);
  });

  target.addEventListener("mouseup", () => {
    clearTimeout(timer);
  });

  target.addEventListener("mouseleave", () => {
    clearTimeout(timer);
  });
}

// document.addEventListener('DOMContentLoaded', async e => {
//   render_messages()
//   post_message()
//   setInterval(get_message, 4000)
//   attach_preview_files()
//   select_chats()
// })

let is_clicked = false
let slide_in = document.querySelector('.slide-in')
delete_multiple.addEventListener('click', e => {
  slide_in.classList.toggle('active')
  if(is_clicked){
    is_clicked = true
    return
  }
})

const chat_profile_js =() => {
  let profile_div = document.querySelector('.profile-panel')
  let media_section = profile_div.querySelector('.media.section')
  let media_section_header = media_section.querySelector('.header')
  let media_section_media = media_section.querySelector('.media-grid')
  let close_profile_btn = profile_div.querySelector('#closeProfile')

  close_profile_btn.onclick = () => {
    document.body.classList.remove('show-profile')
  }
  
  let media_section_is_active = false
  media_section_header.addEventListener('click', async e => {
    if(e.target.classList.contains('category')){
      return
    }
    media_section_header.classList.toggle('active')
    media_section_media.classList.toggle('active')
    media_section_header.querySelector('.down-icon').classList.toggle('active')

    if(!media_section_header.classList.contains('active')){
      media_section_is_active = true
      return
    }


    let url = `/chat-api/get-chat-media/${chat_link}`
    let res = await fetch(url)
    let data = await res.json()

    if(!res.ok){
      console.log(data)
      return
    }
    Array.from(media_section_media.children).forEach(child => {child.classList.add('hidden')})

    data.files.forEach(file => {
      let img = document.createElement('img')
      img.src = file.path
      setTimeout(() => {media_section_media.appendChild(img)}, 1000)
    })
    
  }) 
}