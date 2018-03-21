let ShowUser = React.createClass({

    getInitialState: function() {
        return {
            user: []
        }
    },

    componentDidMount: function() {
        axios.get("/getUser").then(results =>{
            console.log(results.data)
            this.setState({
                user: results.data

            })
        })

    },

    render: function() {

        return (
            <div className="container">
                  <a href="/deleteAccount" className="btn btn-danger btn-lg" style={{float: "right"}} name="deleteAccount">Delete Account</a>
                <h2>Edit Account</h2>
                <form action="/editAccountView" method="post">
                    <div className="form-group">
                        <label for="name">Name:</label>
                        <input type="text" className="form-control" id="name" name="name" placeholder={this.state.user['name']}></input>
                    </div>
                    <div className="form-group">
                        <label for="email">Email:</label>
                        <input type="email" className="form-control" id="email" name="email" placeholder={this.state.user['email']}></input>
                    </div>
                    <div className="form-group">
                        <label for="password1">Password:</label>
                        <input type="password" className="form-control" id="password1" name="passwordForm" placeholder="Leave Blank to Keep Current Password"></input>
                    </div>
                    <div className="form-group">
                        <label for="password2">Confirm Password:</label>
                        <input type="password" className="form-control" id="password2" placeholder="Leave Blank to Keep Current Password"></input>
                    </div>
                        <input type="submit" className="btn btn-success" name="updateAccountButton" value="Edit Account"/>
                </form>
            </div>
        )
    }

})


ReactDOM.render(<ShowUser/>, mountNode);
