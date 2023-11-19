"""Added scripts column

Revision ID: bc9537c54115
Revises: 5abbd9a85969
Create Date: 2023-11-15 15:04:38.554803

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'bc9537c54115'
down_revision: Union[str, None] = '5abbd9a85969'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_exam_id', table_name='exam')
    op.drop_table('exam')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('exam',
    sa.Column('id', mysql.VARCHAR(length=36), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_exam_id', 'exam', ['id'], unique=False)
    # ### end Alembic commands ###