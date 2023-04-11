class BSTNode:
    """
    A Binary Search Tree (BST) node representing a player in an NBA season, with player stats as node data.
    The BST is ordered by the players' points per game (pts_per_g).

    Attributes
    ----------
    player_data : dict
        The data associated with the node, representing a player's stats.
    left : BSTNode
        A reference to the left child of the node.
    right : BSTNode
        A reference to the right child of the node.

    Methods
    -------
    insert(new_player_data: dict) -> None
        Inserts new player data into the tree, following the BST property (smaller values to the left, 
        larger or equal values to the right), based on the player's points per game.
    find_closest(target_pts: float, current_closest: dict) -> dict
        A recursive function that searches the BST for the player with the scoring average closest to the 
        target value, returning the player data dictionary.
    """
    def __init__(self, player_data):
        self.player_data = player_data
        self.left = None
        self.right = None

    def insert(self, new_player_data):
        if float(new_player_data["pts_per_g"]) < float(self.player_data["pts_per_g"]):
            if self.left is None:
                self.left = BSTNode(new_player_data)
            else:
                self.left.insert(new_player_data)
        else:
            if self.right is None:
                self.right = BSTNode(new_player_data)
            else:
                self.right.insert(new_player_data)

    def find_closest(self, target_pts, current_closest):
        current_pts = float(self.player_data["pts_per_g"])
        current_diff = abs(current_pts - target_pts)
        closest_pts = float(current_closest["pts_per_g"])
        closest_diff = abs(closest_pts - target_pts)

        if current_diff < closest_diff:
            current_closest = self.player_data

        if target_pts < current_pts and self.left:
            return self.left.find_closest(target_pts, current_closest)
        elif target_pts > current_pts and self.right:
            return self.right.find_closest(target_pts, current_closest)
        else:
            return current_closest