let ShowPlaylists = React.createClass({

    getInitialState: function() {
        return {
            playlists: [],
            asc: 0
        }
    },

    componentDidMount: function() {
        axios.get("/getPlaylists?asc="+this.state.asc).then(results =>{
            console.log(results.data)
            this.setState({
                playlists: results.data
            })
        })

    },

    changeAsc: function(asc) {
        axios.get("/getPlaylists?asc="+asc).then(results =>{
            console.log(results.data)
            this.setState({
                playlists: results.data
            })
        })
    },


    render: function() {

        return (
            <div>
                <div className="container">
    <h2>My PlayLists</h2>
    <a href="/createPlayList" className="btn btn-success" style={{float: "right"}}>Create New PlayList</a>
    <table className="table table-hover">
        <thead>
        <tr>
            <th>Name <a  onClick={(event) => this.changeAsc(1)} style={{cursor: "pointer"}}><span className="glyphicon glyphicon-chevron-up" style={{color: "black"}}></span></a><a onClick={(event) => this.changeAsc(2)} style={{cursor: "pointer"}}><span className="glyphicon glyphicon-chevron-down" style={{color: "black"}}></span></a></th>
            <th>Size <a onClick={(event) => this.changeAsc(3)} style={{cursor: "pointer"}}><span className="glyphicon glyphicon-chevron-up" style={{color: "black"}}></span></a><a onClick={(event) => this.changeAsc(4)} style={{cursor: "pointer"}}><span className="glyphicon glyphicon-chevron-down" style={{color: "black"}}></span></a></th>
            <th>Creation Date <a onClick={(event) => this.changeAsc(5)} style={{cursor: "pointer"}}><span className="glyphicon glyphicon-chevron-up" style={{color: "black"}}></span></a><a onClick={(event) => this.changeAsc(6)} style={{cursor: "pointer"}}><span className="glyphicon glyphicon-chevron-down" style={{color: "black"}}></span></a></th>
            <th>Songs</th>
            <th>Edit</th>
            <th>Delete</th>
        </tr>
        </thead>

        <tbody>
            {this.state.playlists.map((playlist) =>{
                return (
                    <tr>
                        <td>{playlist["name"]}</td>
                        <td>{playlist["size"]}</td>
                        <td>{playlist["creation_date"]}</td>
                        <td><a key={playlist["id"]} href={'/myPlayListSongs?id='+playlist["id"]} className="btn btn-warning"><span className="glyphicon glyphicon-music"></span></a></td>
                        <td><a key={playlist["id"]} href={'/myPlayListEdit?pID='+playlist["id"]} className="btn btn-info"><span className="glyphicon glyphicon-edit"></span></a></td>
                        <td><a key={playlist["id"]} href={'/myPlayListDel?id='+playlist["id"]} className="btn btn-danger"><span className="glyphicon glyphicon-remove"></span></a></td>
                    </tr>
                )
            })}
        </tbody>



    </table>
</div>
            </div>
        )
    }

})


ReactDOM.render(<ShowPlaylists/>, mountNode);
