"""Init

Revision ID: 428fbaec4e1
Revises: 363c2939b276
Create Date: 2014-06-19 20:14:43.352425

"""

# revision identifiers, used by Alembic.
revision = '428fbaec4e1'
down_revision = '363c2939b276'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contacts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstName', sa.String(length=255), nullable=True),
    sa.Column('lastName', sa.String(length=255), nullable=True),
    sa.Column('emailAddress', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_contacts_lastName', 'contacts', ['lastName'], unique=False)
    op.create_table('inboxes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userMail', sa.String(length=255), nullable=True),
    sa.Column('account', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('server', sa.String(length=255), nullable=True),
    sa.Column('port', sa.String(length=255), nullable=True),
    sa.Column('protocol', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_inboxes_password', 'inboxes', ['password'], unique=False)
    op.create_table('mails',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.String(length=255), nullable=True),
    sa.Column('subject', sa.String(length=255), nullable=True),
    sa.Column('_from', sa.String(length=255), nullable=True),
    sa.Column('to', sa.String(length=255), nullable=True),
    sa.Column('cc', sa.Text(), nullable=True),
    sa.Column('bcc', sa.Text(), nullable=True),
    sa.Column('inReplyTo', sa.String(length=255), nullable=True),
    sa.Column('message', sa.String(length=255), nullable=True),
    sa.Column('inboxId', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['inboxId'], ['inboxes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_mails_inReplyTo', 'mails', ['inReplyTo'], unique=False)
    op.create_index('ix_mails_message', 'mails', ['message'], unique=False)
    op.create_index('ix_mails_subject', 'mails', ['subject'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_mails_subject', 'mails')
    op.drop_index('ix_mails_message', 'mails')
    op.drop_index('ix_mails_inReplyTo', 'mails')
    op.drop_table('mails')
    op.drop_index('ix_inboxes_password', 'inboxes')
    op.drop_table('inboxes')
    op.drop_index('ix_contacts_lastName', 'contacts')
    op.drop_table('contacts')
    ### end Alembic commands ###
