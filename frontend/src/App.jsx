import React, {useState, useEffect} from 'react'
import axios from 'axios'

export default function App(){
  const [projects, setProjects] = useState([])
  const [tasks, setTasks] = useState([])
  const [token, setToken] = useState(localStorage.getItem('token') || '')

  useEffect(()=>{
    if(token){
      axios.get('/api/projects/', { headers: { Authorization: `Bearer ${token}` } })
        .then(r=>setProjects(r.data)).catch(()=>{})
      axios.get('/api/tasks/', { headers: { Authorization: `Bearer ${token}` } })
        .then(r=>setTasks(r.data)).catch(()=>{})
    }
  },[token])

  const loginAs = (role) => {
    const email = role === 'Admin' ? 'admin@example.com' : role === 'Manager' ? 'manager@example.com' : 'dev@example.com'
    axios.post('/api/auth/login', { email, password: 'pass' }).then(r=>{
      setToken(r.data.access_token)
      localStorage.setItem('token', r.data.access_token)
    })
  }

  return (
    <div style={{padding:20,fontFamily:'sans-serif'}}>
      <h1>Project Management Tool (Demo)</h1>
      <div>
        <button onClick={()=>loginAs('Admin')}>Login as Admin</button>
        <button onClick={()=>loginAs('Manager')}>Login as Manager</button>
        <button onClick={()=>loginAs('Developer')}>Login as Developer</button>
        <button onClick={()=>{ localStorage.removeItem('token'); setToken('');}}>Logout</button>
      </div>

      <h2>Projects</h2>
      <pre>{JSON.stringify(projects, null, 2)}</pre>

      <h2>Tasks</h2>
      <pre>{JSON.stringify(tasks, null, 2)}</pre>
    </div>
  )
}
