import { AppLayout } from "./components/AppLayout"
import { Commands } from "./views/Commands"
import { Dashboard } from "./views/Dashboard"
import { Tickets } from './views/Tickets'
import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom"
import { EditCommandModal } from "../components/EditCommandModal"

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<AppLayout/>}>
            <Route index element={<Navigate to={"/dashboard"} replace/>}/>
            <Route path="dashboard" element={<Dashboard />}/>
            <Route path="commands" element={<Commands />}/>
            <Route path="tickets" element={<Tickets />}/>
          </Route>
          <Route path="*" element={<h2>Not found</h2>} />
        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App
