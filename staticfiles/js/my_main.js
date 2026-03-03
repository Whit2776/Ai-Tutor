const create_model_instance = async (url, formdata, redirect = true) => {
    let res = await fetch(url, {method:'POST', body: formdata})
    let res_json = await res.json()
    console.log(res_json)
    if (!res.ok){
      return {success:false}
    }

    if (redirect){
      if (res_json.redirect_url){
        location.href = res_json.redirect_url
      }
    }

    return res_json
}