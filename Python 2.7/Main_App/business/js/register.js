class Register extends React.Component {

  render() {
    return (


        <div className="container">
            <h2>Create Account</h2>
            <form action="/register" method="post">
                <div className="form-group">
                    <label for="name">Name:</label>
                    <input type="text" className="form-control" id="name" name="name" placeholder='Enter Name' required></input>
                </div>
                <div className="form-group">
                    <label for="email">Email:</label>
                    <input type="email" className="form-control" id="email" name="email" placeholder='Enter Email' required></input>
                </div>
                <div className="form-group">
                    <label for="password1">Password:</label>
                    <input type="password" className="form-control" id="password1" name="passwordForm" placeholder="Enter Password"></input>
                </div>
                <div className="form-group">
                    <label for="password2">Confirm Password:</label>
                    <input type="password" className="form-control" id="password2" placeholder="Confirm Password"></input>
                </div>
                <input type="submit" className="btn btn-success" name="updateAccountButton" value="Create Account"/>
            </form>
        </div>


    );
  }
}


ReactDOM.render(<Register />, document.getElementById('mountNode'));
