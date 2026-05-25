import Dashboard from "./Dashboard";
import Login from "./Login";

function App() {

    const token =
        localStorage.getItem("access");

    return (

        <div>

            {
                token
                ?
                <Dashboard />
                :
                <Login />
            }

        </div>
    );
}

export default App;