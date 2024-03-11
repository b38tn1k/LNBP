"""club_stylez

Revision ID: 36b2d063e6eb
Revises: dddf53ed264e
Create Date: 2024-01-26 12:26:53.286904

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '36b2d063e6eb'
down_revision = 'dddf53ed264e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    """
    This function adds a new column 'portal_style' to the 'club' table with a
    maximum length of 100 characters and allows it to be null (i.e., optional).

    """
    op.add_column('club', sa.Column('portal_style', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    """
    This function `downgrade()` drops a column named `portal_style` from a table
    named `club`.

    """
    op.drop_column('club', 'portal_style')
    # ### end Alembic commands ###