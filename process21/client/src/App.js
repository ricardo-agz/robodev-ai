import React from "react";
import './App.css';
import { Routes, Route } from "react-router-dom";
import Home from './Home';
import { Users, UserShow, UserNew, UserEdit } from './pages/user/index';
import { PaymentMethods, PaymentMethodShow, PaymentMethodNew, PaymentMethodEdit } from './pages/paymentMethod/index';
import { MonthlyPledges, MonthlyPledgeShow, MonthlyPledgeNew, MonthlyPledgeEdit } from './pages/monthlyPledge/index';
import { WorkoutPlans, WorkoutPlanShow, WorkoutPlanNew, WorkoutPlanEdit } from './pages/workoutPlan/index';
import { WorkoutGroups, WorkoutGroupShow, WorkoutGroupNew, WorkoutGroupEdit } from './pages/workoutGroup/index';
import { UserContext } from './hooks/UserContext';
import useFindUser from './hooks/useFindUser';
import PrivateRoute from './auth/PrivateRoute';
import Login from './auth/Login';
import Nav from './components/Nav'


function App() {
	const { user, setUser } = useFindUser();

  return (
		<UserContext.Provider value={{ authUser: user, setAuthUser: setUser }}>
    <div className="App">
			<Nav/>
      <Routes>
        <Route path="/" element={<Home />} />

				{/* AUTH */}
				<Route path='/login' element={<Login />} />
				<Route path='/register' element={<UserNew />} />

				{/* User */}
				<Route
					path='/users'
					element={ <PrivateRoute component={<Users />} />}
				/>
				<Route
					path='/user/:id'
					element={ <PrivateRoute component={<UserShow />} />}
				/>
				<Route path='/user/new' element={<UserNew />} />
				<Route
					path='/user/:id/edit'
					element={ <PrivateRoute component={<UserEdit />} />}
				/>

				{/* PaymentMethod */}
				<Route path='/paymentmethods' element={<PaymentMethods />} />
				<Route path='/paymentmethod/:id' element={<PaymentMethodShow />} />
				<Route path='/paymentmethod/new' element={<PaymentMethodNew />} />
				<Route path='/paymentmethod/:id/edit' element={<PaymentMethodEdit />} />

				{/* MonthlyPledge */}
				<Route path='/monthlypledges' element={<MonthlyPledges />} />
				<Route path='/monthlypledge/:id' element={<MonthlyPledgeShow />} />
				<Route path='/monthlypledge/new' element={<MonthlyPledgeNew />} />
				<Route path='/monthlypledge/:id/edit' element={<MonthlyPledgeEdit />} />

				{/* WorkoutPlan */}
				<Route path='/workoutplans' element={<WorkoutPlans />} />
				<Route path='/workoutplan/:id' element={<WorkoutPlanShow />} />
				<Route path='/workoutplan/new' element={<WorkoutPlanNew />} />
				<Route path='/workoutplan/:id/edit' element={<WorkoutPlanEdit />} />

				{/* WorkoutGroup */}
				<Route path='/workoutgroups' element={<WorkoutGroups />} />
				<Route path='/workoutgroup/:id' element={<WorkoutGroupShow />} />
				<Route path='/workoutgroup/new' element={<WorkoutGroupNew />} />
				<Route path='/workoutgroup/:id/edit' element={<WorkoutGroupEdit />} />
      </Routes>  
    </div>
		</UserContext.Provider>
  );
}

export default App;
