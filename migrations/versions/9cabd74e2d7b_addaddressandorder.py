"""'addAddressAndOrder'

Revision ID: 9cabd74e2d7b
Revises: cd91d7a764a7
Create Date: 2020-05-28 09:21:09.514231

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9cabd74e2d7b'
down_revision = 'cd91d7a764a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('member_address',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('member_id', sa.Integer(), nullable=False),
    sa.Column('nickname', sa.String(length=20), nullable=False),
    sa.Column('mobile', sa.String(length=11), nullable=False),
    sa.Column('province_id', sa.Integer(), nullable=False),
    sa.Column('province_str', sa.String(length=50), nullable=False),
    sa.Column('city_id', sa.Integer(), nullable=False),
    sa.Column('city_str', sa.String(length=50), nullable=False),
    sa.Column('area_id', sa.Integer(), nullable=False),
    sa.Column('area_str', sa.String(length=50), nullable=False),
    sa.Column('address', sa.String(length=100), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('is_default', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['member_id'], ['member.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pay_order',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_sn', sa.String(length=40), nullable=False),
    sa.Column('total_price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('yun_price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('pay_price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('pay_sn', sa.String(length=128), nullable=False),
    sa.Column('prepay_id', sa.String(length=128), nullable=False),
    sa.Column('note', sa.Text(), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('express_status', sa.Integer(), nullable=False),
    sa.Column('express_address_id', sa.Integer(), nullable=False),
    sa.Column('express_info', sa.String(length=100), nullable=False),
    sa.Column('comment_status', sa.Integer(), nullable=False),
    sa.Column('pay_time', sa.DateTime(), nullable=False),
    sa.Column('member_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['member_id'], ['member.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('order_sn')
    )
    op.create_table('pay_order_item',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('note', sa.Text(), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('pay_order_id', sa.Integer(), nullable=False),
    sa.Column('member_id', sa.Integer(), nullable=False),
    sa.Column('food_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['food_id'], ['food.id'], ),
    sa.ForeignKeyConstraint(['member_id'], ['member.id'], ),
    sa.ForeignKeyConstraint(['pay_order_id'], ['pay_order.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pay_order_item')
    op.drop_table('pay_order')
    op.drop_table('member_address')
    # ### end Alembic commands ###
