import logging
from app.models import db, Model, ModelProxy, transaction
from app.billing_plans import plans_by_name, FreePlan

logger = logging.getLogger(__name__)

class Team(Model):
    """
    A team is a collection of users sharing the same resources.
    All users get a team. Some teams have more than one member.
    Most resources in the application should belong to a team.

    Usage:
        team.members -> [<TeamMember>, ...]
    """

    id = db.Column(db.Integer(), primary_key=True)
    creator_id = db.Column(db.ForeignKey("user.id"), index=True,
                           nullable=False)

    name = db.Column(db.String(255))
    # Plan may need to become DB backed when billing is introduced.
    plan = db.Column(db.String(), default='free')
    plan_owner_id = db.Column(db.ForeignKey("user.id"))
    subscription_id = db.Column(db.String())
    billing_customer_id = db.Column(db.String())


    creator = db.relationship("User", foreign_keys=[creator_id])
    plan_owner = db.relationship("User", foreign_keys=[plan_owner_id])

    GDPR_EXPORT_COLUMNS = {
        "id": "ID of the team",
        "hashid": "ID of User",
        "name": "Name of the team",
        "plan": "What plan the team was on",
        "created": "When the team was created"
    }

    def has_member(self, user):
        return user in [member.user for member in self.active_members]

    @property
    def is_paid_plan(self):
        return not self.billing_plan.is_free()

    @property
    def billing_plan(self):
        # TODO: Might benefit from a validation to ensure `plan` is a recognized type in billing_plans
        billing_plan = plans_by_name.get(self.plan) or FreePlan
        return billing_plan(self)

    @property
    def active_members(self):
        return [membership for membership in self.members if membership.activated]

    @property
    def active_teams(self):
        return [membership.team for membership in self.members if membership.activated]
    
    @property
    def club(self):
        # Check if the team has club associations.
        if self.club_associations:
            # Loop through the club associations.
            for association in self.club_associations:
                # Return the first associated club.
                if association.club:
                    return association.club
        return None

    @classmethod
    @transaction
    def create(cls, name, creator):
        new_team = cls(name=name, creator=creator)
        new_team_member = ModelProxy.teams.TeamMember(team=new_team, user=creator, role='administrator', activated=True)
        
        # Add the new_team and new_team_member to the session
        db.session.add(new_team)
        db.session.add(new_team_member)
        
        # Flush the session to populate the IDs
        db.session.flush()
        
        # Create the new_club and the association
        new_club = ModelProxy.clubs.Club.create(name=name)
        ModelProxy.clubs.ClubTeamAssociation.create(club_id=new_club.id, team_id=new_team.id)
        
        # Commit the transaction
        db.session.commit()
        
        return new_team
