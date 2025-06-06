"""sync user_id fields

Revision ID: c2d2cc371818
Revises: 9f088083a444
Create Date: 2025-05-26 21:32:14.332480

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'c2d2cc371818'
down_revision: Union[str, None] = '9f088083a444'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('materials', schema=None) as batch_op:
        batch_op.create_foreign_key('fk_materials_user_id', 'users', ['user_id'], ['id'])

    with op.batch_alter_table('subgroups', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_subgroups_user_id', 'users', ['user_id'], ['id'])

    with op.batch_alter_table('tool_transfers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_tool_transfers_user_id', 'users', ['user_id'], ['id'])

    with op.batch_alter_table('tools', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_tools_user_id', 'users', ['user_id'], ['id'])

    with op.batch_alter_table('workers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_workers_user_id', 'users', ['user_id'], ['id'])


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('workers', schema=None) as batch_op:
        batch_op.drop_constraint('fk_workers_user_id', type_='foreignkey')
        batch_op.drop_column('user_id')

    with op.batch_alter_table('tools', schema=None) as batch_op:
        batch_op.drop_constraint('fk_tools_user_id', type_='foreignkey')
        batch_op.drop_column('user_id')

    with op.batch_alter_table('tool_transfers', schema=None) as batch_op:
        batch_op.drop_constraint('fk_tool_transfers_user_id', type_='foreignkey')
        batch_op.drop_column('user_id')

    with op.batch_alter_table('subgroups', schema=None) as batch_op:
        batch_op.drop_constraint('fk_subgroups_user_id', type_='foreignkey')
        batch_op.drop_column('user_id')

    with op.batch_alter_table('materials', schema=None) as batch_op:
        batch_op.drop_constraint('fk_materials_user_id', type_='foreignkey')
