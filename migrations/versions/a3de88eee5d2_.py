"""empty message

Revision ID: a3de88eee5d2
Revises: db0ab370a559
Create Date: 2019-08-29 13:40:44.991231

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a3de88eee5d2'
down_revision = 'db0ab370a559'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cooperative_transactions',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('group_id', sa.Integer(), nullable=False),
                    sa.Column('amount_per_week', sa.Integer(), nullable=False),
                    sa.Column('current_amount', sa.Integer(), nullable=True),
                    sa.Column('membership_status', sa.String(length=16), nullable=True),
                    sa.Column('status', sa.Boolean(), nullable=True),
                    sa.ForeignKeyConstraint(['group_id'], ['group_configuration.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.alter_column('group_configuration', 'amount_per_week',
                    existing_type=mysql.BIGINT(display_width=20),
                    nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('group_configuration', 'amount_per_week',
                    existing_type=mysql.BIGINT(display_width=20),
                    nullable=True)
    op.drop_table('cooperative_transactions')
    # ### end Alembic commands ###
