
let ShowPlaylist = React.createClass({

    getInitialState: function() {
        return {
            playlist: []
        }
    },

    componentDidMount: function() {
        axios.get("/getPlayListInfo").then(results =>{
            console.log(results.data)
            this.setState({
                playlist: results.data

            })
        })

    },

    render: function() {

        return (

            <div className="container">
                <h2>Edit PlayList</h2>
                <form action="/myPlayListEdit" method="post">
                    <div className="form-group">
                        <label for="name">Name:</label>
                        <input type="text" className="form-control" id="name" name="name" placeholder={this.state.playlist['name']}></input>
                    </div>
                        <input type="submit" className="btn btn-success btn-lg btn-block" name="updateAccountButton" value="Edit PlayList"/>
                </form>
            </div>
        )
    }

})


ReactDOM.render(<ShowPlaylist/>, mountNode);

