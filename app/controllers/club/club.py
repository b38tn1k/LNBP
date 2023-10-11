from flask import Blueprint, render_template, abort, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.forms import SimpleForm
from app.forms.club_forms import ClubSetup, FacilitySetup
from app.models import db
from app.models.clubs import Club, Facility

blueprint = Blueprint('club_home', __name__)

@blueprint.before_request
def check_for_membership(*args, **kwargs):
    # Ensure that anyone that attempts to pull up the dashboard is currently an active member
    if not current_user.is_authenticated or current_user.primary_membership_id is None:
        flash('You currently do not have accesss to app', 'warning')
        return redirect(url_for("main.home"))

@blueprint.route('/', methods=["GET", "POST"])
@login_required
def index():
    if current_user.club:
        setup_form = ClubSetup()
        if setup_form.validate_on_submit():
            if setup_form.name.data is not None:
                current_user.club.name = setup_form.name.data

            if setup_form.email.data is not None:
                current_user.club.email = setup_form.email.data

            if setup_form.contact_number.data is not None:
                current_user.club.contact_number = setup_form.contact_number.data
            
            if setup_form.city.data is not None:
                current_user.club.city = setup_form.city.data

            if setup_form.street_address.data is not None:
                street_address_parts = [setup_form.street_address.data]
                if setup_form.street_address2.data is not None:
                    street_address_parts.append(setup_form.street_address2.data)
                current_user.club.street_address = "\n".join(street_address_parts)

            if setup_form.state.data is not None:
                current_user.club.state = setup_form.state.data

            if setup_form.zip_code.data is not None:
                current_user.club.zip_code = setup_form.zip_code.data

            if setup_form.country.data is not None:
                current_user.club.country = setup_form.country.data
            db.session.commit()
            return redirect(url_for('.index'))

        
        setup_form.name.data = current_user.club.name
        setup_form.email.data = current_user.email
        setup_form.contact_number.data = current_user.club.contact_number
        street_address = current_user.club.street_address
        if isinstance(street_address, str):
            address_parts = street_address.split('\n')
            setup_form.street_address.data = address_parts[0] if len(address_parts) > 0 else ""
            setup_form.street_address2.data = address_parts[1] if len(address_parts) > 1 else ""
        setup_form.city.data = current_user.club.city
        setup_form.state.data = current_user.club.state
        setup_form.zip_code.data = current_user.club.zip_code
        setup_form.country.data = current_user.club.country

        facility_form = FacilitySetup()
        
        return render_template('club/club.html', club=current_user.club, setup_form=setup_form, facility_form=facility_form, simple_form=SimpleForm())
    else:
        flash("You are not part of any club", 'warning')

@blueprint.route('/<hashid:club_id>/add-facility', methods=['POST'])
@login_required
def add_facility(club_id):
    club = Club.query.get(club_id)

    form = FacilitySetup()  # Assuming the form's class name is FacilityForm

    if form.validate_on_submit():
        facility_name = form.name.data
        facility_type = form.facility_type.data
        club.add_facility(facility_name, facility_type, current_user, club)

    return redirect(url_for('.index'))

@blueprint.route('/<hashid:facility_id>/delete-facility', methods=['POST'])
@login_required
def delete_facility(facility_id):
    f = Facility.query.get(facility_id)
    if f:
        db.session.delete(f)
        db.session.commit()
    #TODO: delete this shiz
    return redirect(url_for('.index'))

        

