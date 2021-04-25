from .base import *

@dataclass
class UsersData:
	id: str
	login: str
	display_name: str
	type: str
	broadcaster_type: str
	description: str
	profile_image_url: str
	offline_image_url: str
	view_count: int
	email: Optional[str]
	created_at: str


@dataclass
class UsersModel:
	data: List[UsersData]



@dataclass
class UsersFollowsData:
	from_id: str
	from_login: str
	from_name: str
	to_id: str
	to_login: str
	to_name: str
	followed_at: str


@dataclass
class UsersFollowsModel:
	total: int
	pagination: Pagination
	data: List[UsersFollowsData]