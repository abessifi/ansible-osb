# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'spec_helper'
require 'wls_params'

describe "Check for prerequisites" do

  describe "in centos 7 distribution", :if => (os[:family] == 'redhat' && os[:release].start_with?('7.2')) do
    describe package('jdk1.8.0_77') do
      it { should be_installed }
    end
    describe command('java -version') do
      its(:stderr) { should include 'java version "1.8.0' }
    end
  end

  describe group('oinstall') do
    it { should exist }
  end

  describe user('oracle') do
    it { should exist }
    it { should belong_to_group 'oinstall' }
  end

  describe file('/etc/oraInst.loc')do
    it { should exist }
    it { should contain 'inventory_loc=/u01/app/oracle/inventory' }
    it { should contain 'inst_group=oinstall' }
  end

  describe file(ORACLE_MIDDLEWARE_DIR) do
    it { should be_directory }
    it { should be_owned_by 'oracle' }
    it { should be_grouped_into 'oinstall' }
  end

end

